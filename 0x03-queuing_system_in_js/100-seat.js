import { createClient } from 'redis';
import { createQueue } from 'kue';
import { promisify } from 'util';
import express from 'express';

const redisClient = createClient();

// Event listener
redisClient.on('connect', function() {
  console.log('Redis client connected to the server');
});

// Event listener for Redis connection errors
redisClient.on('error', function(err) {
  console.log(`Redis client not connected to the server: ${err}`);
});

const asyncGet = promisify(redisClient.get).bind(redisClient);

// Func to set the num of available seats
function reserveSeat(number) {
  redisClient.set('available_seats', number);
}

// Func to get the current num of available seats
async function getCurrentAvailableSeats() {
  const seats = await asyncGet('available_seats');
  return seats;
}

let reservationEnabled = true;

const queue = createQueue();

// Create an Express app
const app = express();

// Route to get the num of available seats
app.get('/available_seats', async function(req, res) {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({"numberOfAvailableSeats": availableSeats});
});

// Route to reserve a seat
app.get('/reserve_seat', function(req, res) {
  if (!reservationEnabled) {
    res.json({"status": "Reservations are blocked"});
    return;
  }
  // Create a job to reserve a seat
  const job = queue.create('reserve_seat', {'seat': 1}).save((error) => {
    if (error) {
      res.json({"status": "Reservation failed"});
      return;
    } else {
      res.json({"status": "Reservation in process"});
      job.on('complete', function() {
        console.log(`Seat reservation job ${job.id} completed`);
      });
      job.on('failed', function(error) {
        console.log(`Seat reservation job ${job.id} failed: ${error}`);
      });
    }
  });
});

// Route
app.get('/process', function(req, res) {
  res.json({"status": "Queue processing"});
  // Process the reserve_seat jobs in the queue
  queue.process('reserve_seat', async function(job, done) {
    const seat = Number(await getCurrentAvailableSeats());
    if (seat === 0) {
      reservationEnabled = false;
      done(Error('Not enough seats available'));
    } else {
      reserveSeat(seat - 1);
      done();
    }
  });
});

// Start the Express server on port 1245
const port = 1245;
app.listen(port, () => {
  console.log(`App is listening at http://localhost:${port}`);
});

// Initialize num of available seats
reserveSeat(50);
