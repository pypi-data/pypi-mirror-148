from multiprocessing import Process
from time import sleep

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from exceptions import ConfigInvalidException, WebDriverInitialisationException, NoLoginCandidatesFoundException
from exceptions import SiteNotResolvableException
from logmgmt import logger
from model.backend_information import BackendInformation
from model.process_type import ProcessType
from processes.generic_process import GenericAnalysisProcess
from processes.process_helper import ProcessHelper
from services.driver_manager import DriverManager
from services.rest_client import RestClient


def process_function(sso_detection, backend_info: BackendInformation, analysis_run_id: int, config_directory):
    success = False
    rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
    chromedriver = None
    cause = "Unknown"
    try:
        sso_detection_index = sso_detection['index']
        sso_base_page = sso_detection['page']['basePage']
        sso_provider = sso_detection['ssoProvider']['providerName'].title()
        logger.info("Received site " + sso_base_page + " to analyse privacy issues with " + sso_provider)
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 0,
                                                                    "Starting chromedriver")
        chromedriver = DriverManager.generate_driver(config_directory, allow_running_insecure_content=True,
                                                     remove_response_csp_headers=True)
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 15,
                                                                    "Checking config")
        if not ProcessHelper.check_log_in_state(chromedriver):
            raise ConfigInvalidException()
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 30,
                                                                    "Resolving site")
        test_resolve = ProcessHelper.resolve_tld1(chromedriver, sso_base_page)
        if test_resolve is None:
            raise SiteNotResolvableException()
        del chromedriver.requests
        logger.info("Performing privacy detection actions for sso detection with id " + str(sso_detection_index))
        logger.info("Opening site")
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 45,
                                                                    "Opening page")
        chromedriver.get(sso_base_page)
        sleep(10)
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 60,
                                                                    "Performing click actions")
        PrivacyDetectionProcess.find_clickable_element_without_url_change(chromedriver)
        sleep(1)
        logger.info("Performing key actions")
        chromedriver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        sleep(1)
        chromedriver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        sleep(1)
        chromedriver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_UP)
        sleep(1)
        chromedriver.find_element(By.TAG_NAME, "body").send_keys(Keys.HOME)
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 75,
                                                                    "Taking screenshot")
        logger.info("Waiting 10 seconds")
        sleep(10)
        logger.info("Taking screenshot")
        screen = chromedriver.get_screenshot_as_png()
        logger.info("Saving HAR and Screenshot for analysis")
        rest_client.update_progress_of_analysis_using_sso_detection(analysis_run_id, sso_detection_index, 90,
                                                                    "Uploading results")
        success = rest_client.save_privacy_detection(sso_detection_index, analysis_run_id, screen, chromedriver.har)
    except TimeoutException as err:
        cause = "Timout: " + err.__class__.__name__
        logger.error("Timeout reached: " + err.msg)
    except SiteNotResolvableException:
        cause = "Not resolvable"
        logger.error("Could not resolve site!")
    except NoLoginCandidatesFoundException:
        cause = "No login candidates found"
        logger.error("Could not find any login candidates for site")
    except WebDriverException as err:
        cause = "Webdriver problem: " + err.__class__.__name__
        logger.error("Could not finish analysing (" + err.msg + ")!")
    except ConfigInvalidException:
        cause = "Invalid config"
        logger.error("Config is invalid! Could not find exactly one logged in profile (see log before)")
        if rest_client.unregister_currently_in_work_sso_det(analysis_run_id, sso_detection['index']):
            logger.error("Unregistered page at brain.")
            success = True
        else:
            logger.error("Failed unregistering page at brain")
        exit(70)
    except KeyboardInterrupt as err:
        logger.info("Received interrupt. Will deregister current page:")
        logger.info("Done") if rest_client.unregister_currently_in_work_sso_det(analysis_run_id, sso_detection[
            'index']) else logger.error("Failed!")
        success = True
        raise err
    except WebDriverInitialisationException as e:
        logger.error(e)
        logger.error(
            "Webdriver could not be initialized (" + e.thrown_exception.__class__.__name__ + "). This client looks broken. Exit with error code")
        try:
            rest_client.unregister_currently_in_work_sso_det(analysis_run_id, sso_detection['index'])
            rest_client.update_latest_activity("ERROR!")
        except Exception as err:
            logger.error("Could not unregister sso detection and send ERROR status to brain: " +
                         str(err.__class__.__name__) + ": " + str(err))
            pass
        exit(75)
    except Exception as err:
        cause = "Unknown error: " + err.__class__.__name__
        logger.error("Unknown error! This should be managed explicitly " +
                     str(err.__class__.__name__) + ": " + str(err))
    finally:
        if not success:
            try:
                rest_client.unregister_currently_in_work_sso_det_and_block(analysis_run_id, sso_detection['index'],
                                                                           cause)
            except Exception:
                logger.error("Unregistering page at brain did fail!")
        if chromedriver is not None:
            ProcessHelper.quit_chromedriver_correctly(chromedriver)
            del chromedriver.requests, chromedriver


class PrivacyDetectionProcess(GenericAnalysisProcess):

    def prepare(self):
        ProcessHelper.check_for_unfinished_work(self.rest_client)

    def get_next_object_to_analyse(self):
        return self.rest_client.get_next_privacy_detection_page_to_analyse_for_run(self.analysis_run_id)

    def generate_process(self, object_to_analyse) -> Process:
        return Process(target=process_function,
                       args=(object_to_analyse, self.backend_info, self.analysis_run_id,
                             self.config_directory))

    def __init__(self, backend_info, analysis_run_id, process_type, config_directory):
        if process_type is not ProcessType.PRIVACY_DETECTION:
            raise TypeError(str(process_type) + " is not supported for privacy analysis!")
        self.backend_info = backend_info
        self.rest_client = RestClient(backend_info.host, backend_info.port, backend_info.token)
        self.analysis_run_id = analysis_run_id
        self.process_type = process_type
        self.config_directory = config_directory

    @staticmethod
    def find_clickable_element_without_url_change(chromedriver):
        tags = ['body', 'div', 'p']
        for tag in tags:
            elements = chromedriver.find_elements(By.TAG_NAME, tag)
            el_count = len(elements)
            current_el = 0
            logger.info("Checking " + tag + " elements for ability to click (count: " + str(len(elements)) + ")")
            while current_el < len(elements) and current_el < el_count:
                el = elements[current_el]
                current_el += 1
                try:
                    url_before_click = chromedriver.current_url
                    el.click()
                    sleep(1)
                    if url_before_click != chromedriver.current_url:
                        logger.info("Url changed. Reloading page and retrying")
                        chromedriver.get(url_before_click)
                        elements = chromedriver.find_elements(By.TAG_NAME, tag)
                    else:
                        logger.info("Click action performed without url change! Found an valid element.")
                        return el
                except WebDriverException:
                    pass
        logger.warning("We did not find any valid element. Forcing an exception!")
        el = chromedriver.find_element(By.TAG_NAME, 'body')  # Force an exception
        el.click()
        return el
