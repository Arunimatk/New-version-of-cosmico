const axios = require('axios');

const BASE_URL = 'http://localhost:8000';
const API_URL = `${BASE_URL}/api`;

async function verifySystem() {
    console.log("Starting System Verification...");

    // 1. Backend Health
    try {
        const healthRes = await axios.get(`${BASE_URL}/health/`);
        console.log("✅ Backend Health Check: OK", healthRes.data);
    } catch (error) {
        console.error("❌ Backend Health Check: FAILED", error.message);
        // Continue even if failed to check other things? No, backend is critical.
        // But we might want to see if it's connection vs error.
    }

    // 2. Login Reachability
    try {
        await axios.post(`${API_URL}/login`, {});
    } catch (error) {
        if (error.response) {
            if (error.response.status === 404) {
                console.error("❌ Login Endpoint: Not Found (404)");
            } else {
                console.log(`✅ Login Endpoint: Reachable (Status: ${error.response.status})`);
            }
        } else {
            console.error("❌ Login Endpoint: Network Error", error.message);
        }
    }

    // 3. CORS Check
    try {
        const res = await axios.get(`${BASE_URL}/health/`);
        const allowOrigin = res.headers['access-control-allow-origin'];
        console.log(`ℹ️ Access-Control-Allow-Origin: ${allowOrigin || 'Not set or hidden'}`);
    } catch (e) { }

    console.log("Verification checks completed.");
}

verifySystem();
