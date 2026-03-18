from .brain_modules.analytics_dealers import AnalyticsDealersMixin
from .brain_modules.base_mixin import BrainBaseMixin
from .brain_modules.calendar_parser import CalendarParserMixin
from .brain_modules.fun_portal_info import FunPortalInfoMixin
from .brain_modules.intent_routing import IntentRoutingMixin
from .brain_modules.intent_signals import IntentSignalsMixin
from .brain_modules.language_history import LanguageHistoryMixin
from .brain_modules.message_processing import MessageProcessingMixin
from .brain_modules.parking_create import ParkingCreateMixin
from .brain_modules.parking_status import ParkingStatusMixin
from .brain_modules.people_context import PeopleContextMixin
from .brain_modules.people_directory import PeopleDirectoryMixin
from .brain_modules.people_response import PeopleResponseMixin
from .brain_modules.portal_food_help import PortalFoodHelpMixin
from .brain_modules.shared import print
from .brain_modules.weather_workforce_parser import WeatherWorkforceParserMixin
from .brain_modules.weekly_calendar import WeeklyCalendarMixin
from .brain_modules.work_history import WorkHistoryMixin
from .brain_modules.workforce_status import WorkforceStatusMixin


class BrainAIYugii(
    MessageProcessingMixin,
    AnalyticsDealersMixin,
    WorkforceStatusMixin,
    WeatherWorkforceParserMixin,
    FunPortalInfoMixin,
    PeopleResponseMixin,
    PeopleDirectoryMixin,
    WorkHistoryMixin,
    WeeklyCalendarMixin,
    CalendarParserMixin,
    ParkingStatusMixin,
    ParkingCreateMixin,
    PortalFoodHelpMixin,
    LanguageHistoryMixin,
    IntentRoutingMixin,
    IntentSignalsMixin,
    PeopleContextMixin,
    BrainBaseMixin,
):
    """Yugii beyin davranislarini moduler olarak birlestirir."""
    pass


__all__ = ["BrainAIYugii"]


try:
    BrainAIYugii.get_instance()
    print("Yugii Brain ready")
except Exception as e:
    print("Yugii Brain preload hatasi:", e)
