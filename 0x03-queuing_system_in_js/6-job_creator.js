import { createQueue } from "kue";

const queue = createQueue();

const jobData = {
  phoneNumber: "123456271",
  message: "This is my number",
};

const job = queue.create("push_notification_code", jobData).save((err) => {
  if (!err) console.log(`Notification job created: ${job.id}`);
});

job.on("complete", () => console.log("Notification job completed"));
job.on("failed", () => console.log("Notification job failed"));
