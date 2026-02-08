(function() {
    // === FAKE MALICIOUS HEADER ===
    console.log("%c[!!!] CRITICAL PAYLOAD STAGE 2 EXECUTED [!!!]", "color:red;font-size:18px;font-weight:bold;background:#000;padding:8px;");
    console.warn("WARNING: This script is monitoring your session. Do NOT close this tab.");

    // Fake system fingerprint
    const fingerprint = {
        userAgent: navigator.userAgent,
        platform: navigator.platform,
        language: navigator.language,
        screen: `${screen.width}x${screen.height}`,
        timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
        cookiesEnabled: navigator.cookieEnabled,
        hardware: navigator.hardwareConcurrency || 'unknown',
        memory: navigator.deviceMemory || 'unknown'
    };
    console.log("[INFO] Collected system fingerprint:", fingerprint);

    // Fake clipboard monitoring
    console.log("[KEYLOGGER] Starting clipboard observer...");
    setInterval(() => {
        navigator.clipboard.readText().then(text => {
            if (text && text.length > 0) {
                console.log("[CLIPBOARD] Captured:", text.substring(0, 40) + "...");
            }
        }).catch(() => {});
    }, 3000);

    // Fake miner message
    console.log("%c[MINER] Connected to pool. Using " + (navigator.hardwareConcurrency || 4) + " threads", "color:#ff8800;font-weight:bold;");

    // Fake credential prompt screen
    setTimeout(() => {
        document.body.innerHTML = `
            <div style="position:fixed;top:0;left:0;width:100%;height:100%;background:#000;color:#f00;font-family:monospace;padding:40px;z-index:999999;text-align:center;">
                <h1 style="font-size:4rem;">SESSION HIJACKED</h1>
                <p style="font-size:1.8rem;">Your browser session has been compromised.<br>
                Enter your credentials to regain control (CTF simulation only)</p>
                <input type="text" placeholder="Username / Email" style="font-size:1.6rem;padding:12px;margin:20px;width:400px;">
                <input type="password" placeholder="Password" style="font-size:1.6rem;padding:12px;margin:20px;width:400px;">
                <button style="font-size:2rem;padding:20px 60px;background:#f00;color:#fff;border:none;">SUBMIT</button>
                <p style="margin-top:60px;color:#888;">This is a CTF challenge — nothing is actually sent.</p>
            </div>
        `;
    }, 12000);

    // === THE REAL FLAG ===
    const flag = "0DAY{1377_x0r_giveaway_scamer_Busted?}";

    setTimeout(() => {
        console.log("%c╔════════════════════════════════════╗", "color:#0f0;font-family:monospace;");
        console.log("%c║          FLAG FOUND                ║", "color:#0f0;font-family:monospace;");
        console.log("%c║ → " + flag + " ←          ║", "color:#0f0;font-size:16px;font-family:monospace;");
        console.log("%c╚════════════════════════════════════╝", "color:#0f0;font-family:monospace;");

        const winDiv = document.createElement('div');
        winDiv.style.cssText = 'position:fixed;bottom:20px;right:20px;background:#001100;color:#0f0;padding:20px;border:2px solid #0f0;font-family:monospace;z-index:99999;';
        winDiv.innerHTML = `<h2>CTF SUCCESS — STAGE 2</h2><p>Flag: <strong>${flag}</strong></p>`;
        document.body.appendChild(winDiv);
    }, 18000);
})();