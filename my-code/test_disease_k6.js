import http from 'k6/http';
import { check, sleep } from 'k6';

// Define options for the load test
export let options = {
    stages: [
        { duration: '30s', target: 50 },   // Ramp up to 50 VUs over 30 seconds
        { duration: '30s', target: 100 },  // Ramp up to 100 VUs over 30 seconds
        { duration: '1m', target: 200 },   // Stay at 200 VUs for 1 minute
        { duration: '30s', target: 0 },    // Ramp down to 0 VUs over 30 second
    ],
    thresholds: {
        http_req_duration: ['p(95)<500'], // 95% of requests should be below 500ms
    },
};

// Define the base URL of the API
const BASE_URL = 'http://127.0.0.1:8000/api/diseases/';

// Define test parameters (query params)
let params = {
    headers: { 'Content-Type': 'application/json' },
};

// Define the test for the API
export default function () {
    let search_term = 'cholera';  // Example search term
    let page = Math.floor(Math.random() * 5) + 1;  // Randomize page number (1 to 5)

    // Construct the URL with query parameters
    let url = `${BASE_URL}?search=${search_term}&page=${page}`;

    // Send a GET request to the API
    let res = http.get(url, params);

    // Check if the response status is 200 (OK)
    check(res, {
        'is status 200': (r) => r.status === 200,
        'is response valid': (r) => r.body.indexOf('error') === -1,  // Ensure there is no error in the response
    });

    // Simulate user waiting time between requests
    sleep(1);
}
