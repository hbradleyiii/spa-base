/**
 * SPA-base Vue Application
 */

import axios from 'axios';
import axiosMethodOverride from 'axios-method-override';
import Vue from 'vue';


/**
 * Global axios object
 * For using POST _method={PATCH|PUT|DELETE}, we are using axiosMethodOverride.
 * @see: https://github.com/jacobbuck/axios-method-override
 */
window.axios = axiosMethodOverride(axios);


/**
 * Global vue object
 */
window.vue = new Vue();
