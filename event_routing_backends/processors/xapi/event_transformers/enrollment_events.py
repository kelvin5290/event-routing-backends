"""
Transformers for enrollment related events.
"""

from tincan import Activity, ActivityDefinition, Extensions, LanguageMap, Verb

from event_routing_backends.helpers import get_course_from_id
from event_routing_backends.processors.openedx_filters.decorators import openedx_filter
from event_routing_backends.processors.xapi import constants
from event_routing_backends.processors.xapi.registry import XApiTransformersRegistry
from event_routing_backends.processors.xapi.transformer import XApiTransformer
import logging
logger = logging.getLogger(__name__)



class BaseEnrollmentTransformer(XApiTransformer):
    """
    Base transformer for enrollment events.
    """

    def get_context_activities(self):
        """
        Get context activities for xAPI transformed event.

        Returns:
            `ContextActivities`
        """

        return None
    def extract_username_or_userid(self):
        """
        Extracts username or user_id from event by finding it in context first and falling back to data
        if context does have username key

        Returns:
            str
        """
        logger.info(self.get_data('context') )
        logger.info(self.get_data('data') )
        
        
        username_or_id = self.get_data('data.username') or self.get_data('data.user_id')
        if not username_or_id:
            username_or_id = self.get_data('username') or self.get_data('user_id') 
            if not username_or_id:
                username_or_id = self.get_data('context.username') or self.get_data('context.user_id')
        return username_or_id
        
    @openedx_filter(filter_type="event_routing_backends.processors.xapi.enrollment_events.base_enrollment.get_object")
    def get_object(self):
        """
        Get object for xAPI transformed event.

        Returns:
            `Activity`
        """
        course_id = self.get_data('context.course_id', True)
        object_id = self.get_object_iri('course', course_id)
        course = get_course_from_id(course_id)
        display_name = course['display_name']

        return Activity(
            id=object_id,
            definition=ActivityDefinition(
                type=constants.XAPI_ACTIVITY_COURSE,
                name=LanguageMap(**({constants.EN: display_name} if display_name is not None else {})),
                extensions=Extensions({
                    constants.XAPI_ACTIVITY_MODE: self.get_data('data.mode')
                })
            ),
        )


@XApiTransformersRegistry.register('edx.course.enrollment.activated')
@XApiTransformersRegistry.register('edx.course.enrollment.mode_changed')
class EnrollmentActivatedTransformer(BaseEnrollmentTransformer):
    """
    Transformers for event generated when learner enrolls or gets the enrollment mode changed in a course.
    """
    _verb = Verb(
        id=constants.XAPI_VERB_REGISTERED,
        display=LanguageMap({constants.EN: constants.REGISTERED}),
    )


@XApiTransformersRegistry.register('edx.course.enrollment.deactivated')
class EnrollmentDeactivatedTransformer(BaseEnrollmentTransformer):
    """
    Transformers for event generated when learner un-enrolls from a course.
    """
    _verb = Verb(
        id=constants.XAPI_VERB_UNREGISTERED,
        display=LanguageMap({constants.EN: constants.UNREGISTERED}),
    )


@XApiTransformersRegistry.register('edx.course.grade.passed.first_time')
class CourseGradePassedFirstTimeTransformer(BaseEnrollmentTransformer):
    """
    Transformers for event generated when learner pass course grade first time from a course.
    """
    _verb = Verb(
        id=constants.XAPI_VERB_PASSED,
        display=LanguageMap({constants.EN: constants.PASSED}),
    )


@XApiTransformersRegistry.register('edx.course.grade.now_passed')
class CourseGradeNowPassedTransformer(BaseEnrollmentTransformer):
    """
    Transformers for event generated when learner pass course grade first time from a course.
    """
    _verb = Verb(
        id=constants.XAPI_VERB_PASSED,
        display=LanguageMap({constants.EN: constants.PASSED}),
    )


@XApiTransformersRegistry.register('edx.course.grade.now_failed')
class CourseGradeNowFailedTransformer(BaseEnrollmentTransformer):
    """
    Transformers for event generated when learner pass course grade first time from a course.
    """
    _verb = Verb(
        id=constants.XAPI_VERB_FAILED,
        display=LanguageMap({constants.EN: constants.FAILED}),
    )
