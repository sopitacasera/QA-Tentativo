const fs = require("fs");
const path = require("path");
const { defineConfig } = require("cypress");

module.exports = defineConfig({
  video: false,
  screenshotOnRunFailure: true,
  screenshotsFolder: "reports/screenshots",
  e2e: {
    baseUrl: "https://petstore.swagger.io/v2",
    specPattern: "cypress/e2e/**/*.cy.js",
    supportFile: false,
    responseTimeout: 60000,
    setupNodeEvents(on) {
      on("after:run", (results) => {
        const dir = path.join(__dirname, "reports");
        fs.mkdirSync(dir, { recursive: true });
        fs.writeFileSync(
          path.join(dir, "cypress-results.json"),
          JSON.stringify(results, null, 2),
          "utf8"
        );
      });
    },
  },
});
