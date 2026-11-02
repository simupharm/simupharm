from playwright.sync_api import sync_playwright
import os

url = 'file:///' + os.path.abspath('hplc_simulator.html').replace('\\', '/')
print('Loading:', url)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(2000)
    title = page.title()
    print('Page title:', title)
    
    # Check what global variables exist
    keys = page.evaluate("Object.keys(window).filter(k => !k.startsWith('webkit') && !k.startsWith('on'))")
    print('Window keys sample:', keys[:20])
    
    # Check if app or simulation is attached
    eval_res = page.evaluate("""() => {
        return {
            hasApp: typeof app !== 'undefined',
            hasSim: typeof simulation !== 'undefined',
            hasPhysics: typeof PhysicsEngine !== 'undefined'
        };
    }""")
    print('Evaluation result:', eval_res)
    browser.close()
print('Playwright test completed.')
