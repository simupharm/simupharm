from playwright.sync_api import sync_playwright
import os

url = 'file:///' + os.path.abspath('hplc_simulator.html').replace('\\', '/')

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.wait_for_timeout(1000)
    
    res = page.evaluate('''() => {
        const sim = window.SimuPharma.simulation;
        
        // Test standard analgesic mixture run
        const params = {
            flowRate: 1.0,
            columnTemp: 30,
            wavelength: 254,
            injectionVolume: 10,
            concentration: 100,
            columnType: 'C18',
            sample: 'Mixture',
            gradientProgram: [
                { time: 0, percentB: 10, curve: 'linear' },
                { time: 10, percentB: 70, curve: 'linear' }
            ],
            currentFault: 'none'
        };
        
        const data = sim.generateChromatogramData(params);
        return {
            peaks: data.peaks.map(p => ({
                name: p.name,
                rt: p.rt,
                peakWidth: p.peakWidth,
                height: p.height,
                area: p.area,
                asymmetry: p.asymmetry
            })),
            totalPoints: data.dataA.length,
            timeStart: data.dataA[0].x,
            timeEnd: data.dataA[data.dataA.length - 1].x
        };
    }''')
    print("Simulation execution output:")
    for p in res['peaks']:
        print(f"  {p['name']:<35} tR = {p['rt']:.3f} min, w = {p['peakWidth']:.4f} min, As = {p['asymmetry']:.2f}")
    print(f"Total time points: {res['totalPoints']}, time: {res['timeStart']} to {res['timeEnd']} min")
    
    browser.close()
