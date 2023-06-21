import { createClient, print } from "redis";
import { promisify } from "util";

const client = createClient();
const promisifiedGet = promisify(client.get).bind(client);

client.on("error", (err) =>
  console.log(`Redis client not connected to the server: ${err}`)
);

function setNewSchool(schoolName, value) {
  client.set(schoolName, value, print);
}

function displaySchoolValue(schoolName) {
  return promisifiedGet(schoolName)
    .then((data) => console.log(data))
    .catch((err) => console.log(err));
}

async function main() {
  await displaySchoolValue("Holberton");
  setNewSchool("HolbertonSanFrancisco", "100");
  await displaySchoolValue("HolbertonSanFrancisco");
}

client.on("connect", async () => {
  console.log("Redis client connected to the server");
  await main();
});
