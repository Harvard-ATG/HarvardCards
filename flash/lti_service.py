from flash.models import Collection, Users_Collections, Course_Map, Course

from django_auth_lti import const

import datetime
import logging
import urlparse
log = logging.getLogger(__name__)

class LTIService:
    '''
    This class provides services for when the tool is running as an LTI tool in the context
    of a canvas course.
    '''
    def __init__(self, request):
        self.request = request
        self.course = None
        if self.isLTILaunch() and not self.courseExists():
            self.course = self.createCourse()

    def getResourceLinkId(self):
        return self.getLTILaunchParam('resource_link_id', None)

    def isTeacher(self):
        is_teacher = False
        if self.isLTILaunch():
            if self.hasTeachingStaffRole():
                is_teacher = True
        return is_teacher

    def getCourse(self, course_id=None):
        if course_id is None:
            if self.course is not None:
                return self.course
            course_id = self.getCourseId()
        return Course.objects.get(course_id=course_id)

    def getEntityName(self):
        '''Returns the entity name for the tool consumer.'''
        url = self.getLTILaunchParam('launch_presentation_return_url', None)
        if url is None: 
            entity = 'entity'
        else:
            parts = urlparse.urlsplit(url).netloc.split('.'); 
            if len(parts) >= 2:
                entity = parts[-2]
        return entity.lower()

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

    def getCourseId(self):
        '''Returns the canvas course id associated with the LTI launch.'''
        context_id = self.getContextId()
        entity = self.getEntityName()
        return entity+'_'+context_id

    def getContextId(self):
        return self.getLTILaunchParam('context_id', None)

    def getProductInfo(self):
        return self.getLTILaunchParam('tool_consumer_info_product_family_code', None)

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
        is_teacher = len(role_set.intersection(teaching_staff)) > 0
        return is_teacher

    def courseExists(self):
        '''Returns True if the canvas course exists, otherwise False.'''
        course_id = self.getCourseId()
        return Course.objects.filter(course_id=course_id).exists()

    def createCourse(self):
        '''Creates and returns an instance of the canvas course. Returns False if the canvas course ID is invalid.'''
        canvas_course_id = self.getCanvasCourseId()
        course_id = self.getCourseId()
        entity = self.getEntityName()
        context_id = self.getContextId()
        product_info = self.getProductInfo()

        log.debug("createCourse(): %s" % course_id)
        if course_id is None:
            return False
        course = Course(
            canvas_course_id=canvas_course_id,
            product=product_info,
            course_id=course_id,
            entity=entity,
            context_id=context_id,
            course_name_short=self.getLTILaunchParam('context_label', ''),
            course_name=self.getLTILaunchParam('context_title', ''),

        )
        course.save()
        return course

    def isCourseAssociated(self, course_id, collection_id):
        '''Returns true if the given course ID is associated with the given collection ID, false otherwise.'''
        course = self.getCourse(course_id)
        found = Course_Map.objects.filter(collection__id=collection_id, course=course)
        if found:
            return True
        return False

    def associateCourse(self, collection_id):
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
        if not self.hasTeachingStaffRole():
            return False

        course_id = self.getCourseId()
        if course_id is None:
            log.debug("setupCourseMap(): no course id")
            return False

        log.debug("setupCourseMap(): lookup course id [%s] and collection id [%s]" % (course_id, collection_id))
        if self.isCourseAssociated(course_id, collection_id):
            log.debug("setupCourseMap(): mapping found")
            return True

        collection = Collection.objects.get(id=collection_id)
        subscribe = self.hasTeachingStaffRole()
        course = self.getCourse()

        course_map = Course_Map(course=course, collection=collection, subscribe=subscribe)
        course_map.save()
        log.debug("setupCourseMap(): created mapping [%s]" % course_map.id)
        return True

    def getCourseCollections(self):
        '''Returns the list of collection IDs associated with the canvas course.'''
        if not self.isLTILaunch():
            return []

        course_id = self.getCourseId()
        course = self.getCourse()

        course_maps = Course_Map.objects.filter(course=course)
        collection_ids = [m.collection.id for m in course_maps]

        return collection_ids

    def subscribeToCourseCollections(self):
        '''
        This subscribes the user to instructor-created collections associated with the 
        canvas course that they don't already subscribe to. 
        '''
        if not self.isLTILaunch():
            return False

        course_id = self.getCourseId()
        if course_id is None:
            log.debug("No canvas course id. Aborting.")
            return False
        course = self.getCourse()

        course_maps = Course_Map.objects.filter(course=course, subscribe=True)
        course_collection_ids = [m.collection.id for m in course_maps]
        subscribed = Users_Collections.objects.filter(user=self.request.user, collection__in=course_collection_ids)
        subscribed_collection_ids = [s.collection.id for s in subscribed]

        unsubscribed_collection_ids = set(course_collection_ids).difference(set(subscribed_collection_ids))
        log.debug("Course collections: %s Subscribed: %s Unsubscribed: %s" % (course_collection_ids, subscribed_collection_ids, unsubscribed_collection_ids))
        if len(unsubscribed_collection_ids) == 0:
            log.debug("Nothing to subscribe... done")
            return False

        log.debug("Subscribing user %s to all course collections: %s => %s" % (self.request.user.id, course_id, unsubscribed_collection_ids))
        for collection_id in unsubscribed_collection_ids:
            collection = Collection.objects.get(id=collection_id)
            if self.isTeacher():
                role = Users_Collections.ADMINISTRATOR
            else:
                role = Users_Collections.LEARNER
            uc_values = dict(user=self.request.user, collection=collection, role=role, date_joined=datetime.date.today())
            Users_Collections.objects.get_or_create(**uc_values)

        return True

