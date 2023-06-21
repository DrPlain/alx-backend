import createPushNotificationsJobs from "./8-job.js";
import { createQueue } from "kue";
import { expect } from "chai";
import sinon from "sinon";

describe("createPushNotificationsJobs", () => {
  const queue = createQueue({ name: "push_notification_code_test" });

  before(() => {
    queue.testMode.enter();
    queue.testMode.clear();
  });

  after(() => {
    queue.testMode.clear();
    queue.testMode.exit();
  });

  it("Create two new jobs to the queue", (done) => {
    expect(queue.testMode.jobs.length).to.equal(0);

    const jobsData = [{ phoneNumber: "1234" }, { phoneNumber: "2342" }];

    createPushNotificationsJobs(jobsData, queue);

    expect(queue.testMode.jobs.length).to.equal(2);
    expect(queue.testMode.jobs[0].data).to.deep.equal(jobsData[0]);
    expect(queue.testMode.jobs[0].type).to.equal("push_notification_code_3");

    done();
  });

  it("Display an error message if jobs is not an array", (done) => {
    const jobsData = "not an array";

    // if we directly invoke the function within expect, any error thrown by the function will propagate outside the test
    expect(() => createPushNotificationsJobs(jobsData, queue)).to.throw(
      Error,
      "Jobs is not an array"
    );
    done();
  });
});
