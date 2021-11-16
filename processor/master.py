from processor.portal.login_module import LoginPage
from processor.portal.master_module import RdMaster
from processor.portal.navigation_module import PortalNavigation

if __name__ == '__main__':
    LoginPage.Login()
    PortalNavigation.navigate_to_accounts()
    RdMaster.process_accounts()
    LoginPage.logout()
