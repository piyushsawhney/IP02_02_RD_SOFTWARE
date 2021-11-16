import datetime

from processor.app_config.db_sql import GET_SCHEDULE_NUMBERS
from processor.db.database import execute_select_query
from processor.portal.download_schedule_module import RdDownloadSchedules
from processor.portal.login_module import LoginPage
from processor.portal.navigation_module import PortalNavigation


class ScheduleDownloader:
    @staticmethod
    def get_schedule_details_from_db(date):
        return execute_select_query(GET_SCHEDULE_NUMBERS, (str(date),))


if __name__ == '__main__':
    today_date = datetime.date.today()
    schedule_list = ScheduleDownloader.get_schedule_details_from_db(today_date)
    if schedule_list:
        LoginPage.Login()
        PortalNavigation.navigate_to_reports()
        for schedule in schedule_list:
            RdDownloadSchedules.search_schedule(schedule[0], str(today_date))
            RdDownloadSchedules.download_schedule_excel()
        LoginPage.logout()
