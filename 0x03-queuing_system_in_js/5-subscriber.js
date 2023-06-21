import { createClient, print } from "redis";

const client = createClient();

client.on("error", (err) =>
  console.log(`Redis client not connected to the server: ${err}`)
);

const channel = "holberton school channel";

client.subscribe(channel);

client.on("message", (channel, message) => {
  if (message === "KILL_SERVER") {
    client.unsubscribe(channel);
    client.quit();
  }
  console.log(message);
});

client.on("connect", () => {
  console.log("Redis client connected to the server");
});
