from playwright.async_api import async_playwright
from config import *

DATASET = ""
TEST_ID = ""
TARGET_URL = ""
EXTENSION_ID = ""

async def record_console_errors(data):
    try:
        logging.error(f"""[PAGE ERROR] {data.code}: {data.message}.\n""")
    except:
        logging.error(f"""Error while recording console errors testing for: {EXTENSION_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))

async def get_page_handle(context):
    page = None
    try:
        if not context: return
        page = await context.new_page()
        page.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
        page.on("pageerror", lambda exception: record_console_errors(exception))
    except:
        if page: await page.close()
        logging.error(f""" Error while getting fresh page handle for extension: {EXTENSION_ID} - {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))
    return page

async def browse(context, url):
    page = None
    try:
        page = await get_page_handle(context)
        if not page: raise Exception("Page could not be created!")
        await page.goto(url, **{
            "wait_until": 'load',
            "timeout": CRAWL_TIMEOUT,
        })
        print(f"{page.url}")
        await asyncio.sleep(WAIT_TIMEOUT)
        await page.close()
    except:
        raise Exception(f"""Couldn't successfully visit for extension: {EXTENSION_ID} - {TEST_ID}.""")

async def detect_extension(context):
    page = None
    try:
        page = await get_page_handle(context)
        await page.goto('chrome://extensions', **{
            "wait_until": 'domcontentloaded',
            "timeout": CRAWL_TIMEOUT_II,
        })
        document_handle = await page.evaluate_handle("document.body")
        extensions_handle = await page.evaluate_handle("""document =>
            [...document.querySelectorAll('body > extensions-manager')[0]
                .shadowRoot.querySelector('#items-list')
                .shadowRoot.querySelectorAll('extensions-item')].map(elem => elem.id);""",
                document_handle
        )
        extensions_list = await extensions_handle.json_value()
        await extensions_handle.dispose()
        await page.close()
        return (len(extensions_list) > 0)
    except:
        logging.error(f""" Error while loading or detecting extension: {EXTENSION_ID} - {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))

async def get_browser_context(playwright):
    context = None
    try:
        if os.path.exists(TMP_PATH + TEST_ID):
            shutil.rmtree(TMP_PATH + TEST_ID)
        launch_arg = deepcopy(LAUNCH_ARGS)
        launch_arg["args"].append(f"--disable-extensions-except={EXTENSION_DIR}{TEST_ID}/")
        launch_arg["args"].append(f"--load-extension={EXTENSION_DIR}{TEST_ID}/")
        context = await playwright.chromium.launch_persistent_context(f"{TMP_PATH}{TEST_ID}", **launch_arg)
        if not context: return None
        if not await detect_extension(context):
            await context.close()
            return None
    except:
        logging.error(f""" Error while instantiating browser context for extension: {EXTENSION_ID} - {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))
    return context

async def execute_crawl(playwright):
    retrial = 0
    try:
        while True:
            try:
                context = await get_browser_context(playwright)
                if not context: raise Exception(f"Context could not be created successfuly for extension: {EXTENSION_ID} - {TEST_ID}")
                await browse(context, f"{TARGET_URL}?testId={TEST_ID}&visit={str(0)}&extensionId={EXTENSION_ID}&browser=chrome&dataset={DATASET}")
                await context.close()
                break
            except:
                if context: await context.close()
                if retrial < ALLOWED_RETRIALS: retrial += 1
                else:
                    logging.error(f"""Couldn't succesfully visit for extension: {EXTENSION_ID} - {TEST_ID}: %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))
                    break
        if context: await context.close()
    except: logging.error(f""" Error while executing crawl for extension: {EXTENSION_ID} - {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))

async def parse_arguments():
    global TEST_ID
    global DATASET
    global TARGET_URL
    global EXTENSION_ID
    try:
        DATASET = os.getenv('DATASET')
        TEST_ID = os.getenv('TEST_ID')
        TARGET_URL = os.getenv('URL')
        EXTENSION_ID = os.getenv('EXTENSION_ID')

        if DATASET is None or TEST_ID is None or TARGET_URL is None or EXTENSION_ID is None:
            raise Exception("")

    except:
        logging.error(f""" Invalid arguments passed! : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))
        sys.exit(1)

async def init(playwright):
    try:
        await parse_arguments()
        await execute_crawl(playwright)
        if os.path.exists(TMP_PATH + TEST_ID):
            shutil.rmtree(TMP_PATH + TEST_ID)
        await playwright.stop()
    except: logging.error(f""" Error in init() for extension: {EXTENSION_ID} - {TEST_ID} : %s.\n""" % '; '.join(str(traceback.format_exc()).split('\n')))

async def main():
    async with async_playwright() as playwright:
        await init(playwright)

asyncio.run(main())