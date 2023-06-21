import express from "express";
import { createClient, print } from "redis";
import { promisify } from "util";

const client = createClient();
const promisifiedGet = promisify(client.get).bind(client);

const listProducts = [
  {
    itemId: 1,
    itemName: "Suitcase 250",
    price: 50,
    initialAvaialableQuantity: 4,
  },
  {
    itemId: 2,
    itemName: "Suitcase 450",
    price: 100,
    initialAvaialableQuantity: 10,
  },
  {
    itemId: 3,
    itemName: "Suitcase 650",
    price: 350,
    initialAvaialableQuantity: 2,
  },
  {
    itemId: 4,
    itemName: "Suitcase 1050",
    price: 550,
    initialAvaialableQuantity: 5,
  },
];

/**
 * Gets an item by its id
 * @param {number} id - The id of the item
 * @returns item
 */
const getItemById = (id) => {
  for (const item of listProducts) {
    if (item.itemId === Number(id)) {
      return item;
    }
  }
};

/**
 * Modifies the reserved stock for a given item.
 * @param {number} itemId - The id of the item.
 * @param {number} stock - The stock of the item.
 */
const reserveStockById = (itemId, stock) => {
  client.set(`item.${itemId}`, stock, print);
};

/**
 * Method that gets the keeps track of item's stock
 * @param {itemId} itemId - The id of the item
 * @returns - A promise
 */
const getCurrentReservedStockById = async (itemId) => {
  return await promisifiedGet(`item.${itemId}`);
};

const app = express();

app.get("/list_products", (req, res) => {
  res.json(listProducts);
});

app.get("/list_products/:itemId", async (req, res) => {
  let { itemId } = req.params;
  if (itemId) itemId = Number(itemId);

  let item = getItemById(itemId);
  if (!item) {
    res.json({ status: "Product not found" });
    return;
  }

  let currentQunatity;
  try {
    currentQunatity = await getCurrentReservedStockById(itemId);
  } catch (err) {}

  if (!currentQunatity) {
    res.json({ status: "Product not found" });
  } else {
    item.currentQunatity = currentQunatity;
    res.json(item);
  }
});

app.get("/reserve_product/:itemId", (req, res) => {
  let { itemId } = req.params;
  if (itemId) itemId = Number(itemId);
  if (itemId) {
    const requestedItem = getItemById(itemId);
    if (!requestedItem) {
      res.json({ status: "Product not found" });
    }
    if (requestedItem.initialAvaialableQuantity <= 0) {
      res.json({
        status: "Not enough stock available",
        itemId: itemId,
      });
    }
    reserveStockById(itemId, requestedItem.initialAvaialableQuantity);
    res.json({
      status: "Reservation confirmed",
      itemId: itemId,
    });
  }
});

app.listen(1245);
