const RestAPI = require('../backend/restAPI');
const Constants = require('../utils/constants');
const Config = require('../utils/config');
const RulesManager = require('../rules/rules_manager');
const Logger = require('../utils/logger');
const startHeartbeatTimer = require('../modules/sync');

function login(runtimeInfo) {
    try {
        Config.runtimeInfo = runtimeInfo;
        const restApi = new RestAPI(Constants.REST_API_LOGIN, Config.info);

        if (RulesManager.isAppDeleted()) {
            Logger.write(Logger.ERROR && `Deletion triggered from PO dashboard, this app is no longer protected.`);
            return [];
        }
        const rulesData = restApi.postSync();
        Logger.write(Logger.DEBUG && `Login returned: ${JSON.stringify(rulesData)}`);
        RulesManager.handleIncomingRules(rulesData);
        startHeartbeatTimer();
        return RulesManager.runtimeRules;
    } catch (err) {
        Logger.write(Logger.ERROR && `Failed to call login with error: ${err}`);
        return [];
    }
}

module.exports = login;
