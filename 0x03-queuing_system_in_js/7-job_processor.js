import { createQueue } from "kue";

const queue = createQueue();

const blacklistedNumbers = ["4153518780", "4153518781"];

function sendNotification(phoneNumber, message, job, done) {
  // Updates the progress on kue progress event
  job.progress(0, 100);

  if (blacklistedNumbers.includes(phoneNumber)) {
    const error = new Error(`Phone number ${phoneNumber} is blacklisted`);
    return done(error);
  }

  job.progress(50, 100);

  console.log(
    `Sending notification to ${phoneNumber}, with message: ${message}`
  );
  done();
}

const concurrency = 2;
queue.process("push_notification_code_2", concurrency, (job, done) => {
  sendNotification(job.data.phoneNumber, job.data.message, job, done);
});
