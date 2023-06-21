import { createClient } from "redis";
import { promisify } from "util";
import express from "express";
import { createQueue } from "kue";

const client = createClient();
const app = express();
const queue = createQueue();

const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);
const reservationEnabled = true;

/**
 * Methods that reserves a specific number of seats
 * @param {number} number - Number of available seats
 */
function reserveSeat(number) {
  client.set("available_seats", number);
}

// Initializes available seats to 50
reserveSeat(50);

/**
 * Method that gets the current number of available seats
 * @returns
 */
async function getCurrentAvailableSeats() {
  const seats = await getAsync("available_seats");
  return parseInt(seats);
}

app.get("/available_seats", async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get("/reserve_seat", (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: "Reservation are blocked" });
    return;
  }
  const job = queue.create("reserve_seat");
  job.on("complete", () => console.log(`Seat reservation ${job.id} completed`));
  job.save((err) => {
    if (err) {
      res.json({ status: "Reservation failed" });
    } else {
      res.json({ status: "Reservation in process" });
    }
  });
});

app.get("/process", async (req, res) => {});

app.listen(1245);
