from harvardcards.apps.flash.models import Collection, Users_Collections, Canvas_Course_Map

from django_auth_lti import const

import datetime

import logging
log = logging.getLogger(__name__)

class LTIService:
    def __init__(self, request):
        self.request = request

    def isLTILaunch(self):
        return "LTI_LAUNCH" in self.request.session

    def hasRole(self, role):
        roles = self.request.session["LTI_LAUNCH"].get('roles', [])
        return True
        return role in roles

    def getCanvasCourseId(self):
        return self.request.session['LTI_LAUNCH'].get('custom_canvas_course_id',None)

    def associateCanvasCourse(self, collection_id):
        if not self.isLTILaunch():
            return False
        if not self.hasRole(const.INSTRUCTOR):
            return False

        canvas_course_id = self.getCanvasCourseId()
        if canvas_course_id is None:
            log.debug("setupCanvasCourseMap(): no canvas course id")
            return False

        log.debug("setupCanvasCourseMap(): lookup canvas course id [%s] and collection id [%s]" % (canvas_course_id, collection_id))

        found = Canvas_Course_Map.objects.filter(collection__id=collection_id, canvas_course_id=canvas_course_id)
        if found:
            log.debug("setupCanvasCourseMap(): found mapping")
            return False

        collection = Collection.objects.get(id=collection_id)
        canvas_course_map = Canvas_Course_Map(canvas_course_id=canvas_course_id, collection=collection)
        canvas_course_map.save()
        log.debug("setupCanvasCourseMap(): created mapping [%s]" % canvas_course_map.id)
        return True

    def subscribeToCourseCollections(self):
        if not self.isLTILaunch():
            return False
        if not self.hasRole(const.LEARNER):
            return False

        canvas_course_id = self.getCanvasCourseId()
        if canvas_course_id is None:
            log.debug("No canvas course id")
            return False

        canvas_course_maps = Canvas_Course_Map.objects.filter(canvas_course_id=canvas_course_id)
        canvas_course_collection_ids = [m.collection.id for m in canvas_course_maps]
        subscribed = Users_Collections.objects.filter(user=self.request.user, collection__in=canvas_course_collection_ids)
        subscribed_collection_ids = [s.collection.id for s in subscribed]
    
        unsubscribed_collection_ids = set(canvas_course_collection_ids).difference(set(subscribed_collection_ids))
        log.debug("Canvas course collections: %s - Subscribed: %s - Unsubscribed: %s" % (canvas_course_collection_ids, subscribed_collection_ids, unsubscribed_collection_ids))
        if len(unsubscribed_collection_ids) == 0:
            return False

        log.debug("Preparing to subscribe user [%s] to course [%s] collections [%s]" % (self.request.user.id, canvas_course_id, unsubscribed_collection_ids))
        for collection_id in unsubscribed_collection_ids:
            collection = Collection.objects.get(id=collection_id)
            Users_Collections.objects.create(user=self.request.user, collection=collection, role=Users_Collections.LEARNER, date_joined=datetime.date.today())
        return True

