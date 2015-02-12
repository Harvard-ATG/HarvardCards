from harvardcards.apps.flash.models import Collection, Users_Collections, Canvas_Course_Map, Canvas_Course

from django_auth_lti import const

import datetime

import logging
log = logging.getLogger(__name__)

class LTIService:
    '''
    This class provides services for when the tool is running as an LTI tool in the context
    of a canvas course.
    '''
    def __init__(self, request):
        self.request = request
        if self.isLTILaunch() and not self.canvasCourseExists():
            self.createCanvasCourse()

    def isLTILaunch(self):
        '''Returns true if an LTI launch is detected, false otherwise.'''
        return "LTI_LAUNCH" in self.request.session

    def getLTILaunchParam(self, param, param_default):
        '''Returns an LTI launch parameter saved in the session.'''
        LTI_LAUNCH = self.request.session.get("LTI_LAUNCH", {})
        return LTI_LAUNCH.get(param, param_default)

    def getCanvasCourseId(self):
        '''Returns the canvas course id associated with the LTI launch.'''
        return self.getLTILaunchParam('custom_canvas_course_id', None)

    def hasRole(self, role):
        '''Returns true if the user that initiated the LTI launch has a given role, false otherwise.'''
        return role in self.getLTILaunchParam('roles', [])

    def hasTeachingStaffRole(self):
        '''
        Returns true if the user has at least one of these roles: 
            Administrator, Instructor, or Teaching Assistant in the course.
        '''
        role_set = set(self.getLTILaunchParam('roles', []))
        teaching_staff = set([const.ADMINISTRATOR, const.TEACHING_ASSISTANT, const.INSTRUCTOR])
        role_set.intersection(teaching_staff)
        return len(role_set) > 0

    def canvasCourseExists(self):
        '''Returns True if the canvas course exists, otherwise False.'''
        canvas_course_id = self.getCanvasCourseId()
        return Canvas_Course.objects.filter(canvas_course_id=canvas_course_id).exists()

    def createCanvasCourse(self):
        '''Creates an instance of the canvas course.'''
        canvas_course_id = self.getCanvasCourseId()
        log.debug("createCanvasCourse(): %s" % canvas_course_id)
        canvas_course = Canvas_Course(
            canvas_course_id=canvas_course_id, 
            course_name_short=self.getLTILaunchParam('context_label', ''),
            course_name=self.getLTILaunchParam('context_title', ''),
        )
        canvas_course.save()
        return canvas_course

    def isCanvasCourseAssociated(self, canvas_course_id, collection_id):
        '''Returns true if the given canvas course ID is associated with the given collection ID, false otherwise.'''
        found = Canvas_Course_Map.objects.filter(collection__id=collection_id, canvas_course_id=canvas_course_id)
        if found:
            return True
        return False

    def associateCanvasCourse(self, collection_id):
        '''
        This creates a mapping between a canvas course, the context in which the LTI tool is operating,
        and a given collection. 
        
        If the user that initiated the LTI launch is an instructor, the subscribe flag is enabled. 
        Otherwise, if the user is a student learner, then the subscribe flag is disabled.

        The subscribe flag is used to differentiate instructor-created collections from student-created
        collections. This flag is used to automatically subscribe students to collections created by 
        instructors for the course.
        '''

        if not self.isLTILaunch():
            return False

        canvas_course_id = self.getCanvasCourseId()
        if canvas_course_id is None:
            log.debug("setupCanvasCourseMap(): no canvas course id")
            return False

        log.debug("setupCanvasCourseMap(): lookup canvas course id [%s] and collection id [%s]" % (canvas_course_id, collection_id))
        if self.isCanvasCourseAssociated(canvas_course_id, collection_id):
            log.debug("setupCanvasCourseMap(): mapping found")
            return True

        collection = Collection.objects.get(id=collection_id)
        subscribe = self.hasTeachingStaffRole()
        canvas_course_map = Canvas_Course_Map(canvas_course_id=canvas_course_id, collection=collection, subscribe=subscribe)
        canvas_course_map.save()
        log.debug("setupCanvasCourseMap(): created mapping [%s]" % canvas_course_map.id)
        return True

    def getCourseCollections(self):
        '''Returns the list of collection IDs associated with the canvas course.'''
        if not self.isLTILaunch():
            return []

        canvas_course_id = self.getCanvasCourseId()
        canvas_course_maps = Canvas_Course_Map.objects.filter(canvas_course_id=canvas_course_id)
        canvas_collection_ids = [m.collection.id for m in canvas_course_maps]

        return canvas_collection_ids

    def subscribeToCourseCollections(self):
        '''
        This subscribes the user to instructor-created collections associated with the 
        canvas course that they don't already subscribe to. 
        '''
        if not self.isLTILaunch():
            return False

        canvas_course_id = self.getCanvasCourseId()
        if canvas_course_id is None:
            log.debug("No canvas course id. Aborting.")
            return False

        canvas_course_maps = Canvas_Course_Map.objects.filter(canvas_course_id=canvas_course_id, subscribe=True)
        canvas_course_collection_ids = [m.collection.id for m in canvas_course_maps]
        subscribed = Users_Collections.objects.filter(user=self.request.user, collection__in=canvas_course_collection_ids)
        subscribed_collection_ids = [s.collection.id for s in subscribed]
    
        unsubscribed_collection_ids = set(canvas_course_collection_ids).difference(set(subscribed_collection_ids))
        log.debug("Canvas course collections: %s Subscribed: %s Unsubscribed: %s" % (canvas_course_collection_ids, subscribed_collection_ids, unsubscribed_collection_ids))
        if len(unsubscribed_collection_ids) == 0:
            log.debug("Nothing to subscribe... done")
            return False

        log.debug("Subscribing user %s to all canvas course collections: %s => %s" % (self.request.user.id, canvas_course_id, unsubscribed_collection_ids))
        for collection_id in unsubscribed_collection_ids:
            collection = Collection.objects.get(id=collection_id)
            uc_values = dict(user=self.request.user, collection=collection, role=Users_Collections.LEARNER, date_joined=datetime.date.today())
            Users_Collections.objects.get_or_create(**uc_values)

        return True

