import express from "express";
import { createClient, print } from "redis";
import { promisify } from "util";

const client = createClient();
const promisifiedGet = promisify(client.get).bind(client);

const listProducts = [
  {
    id: 1,
    name: "Suitcase 250",
    price: 50,
    stock: 4,
  },
  {
    id: 2,
    name: "Suitcase 450",
    price: 100,
    stock: 10,
  },
  {
    id: 3,
    name: "Suitcase 650",
    price: 350,
    stock: 2,
  },
  {
    id: 4,
    name: "Suitcase 1050",
    price: 550,
    stock: 5,
  },
];

/**
 * Gets an item by its id
 * @param {number} id - The id of the item
 * @returns item
 */
const getItemById = (id) => {
  for (const item of listProducts) {
    if (item.id === parseInt(id)) {
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
  client.incrby(`item.${itemId}`, stock, print);
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
  const responseList = listProducts.map((product) => {
    const newObj = {};
    for (let key in product) {
      if (key === "id") {
        newObj.itemId = product[key];
      } else if (key === "name") {
        newObj.itemName = product[key];
      } else if (key === "stock") {
        newObj.initialAvaialableQuantity = product[key];
      } else {
        newObj.key = product[key];
      }
    }
    return newObj;
  });
  res.json(responseList);
});

app.get("/list_products/:itemId", async (req, res) => {
  let { itemId } = req.params;
  if (itemId) itemId = parseInt(itemId);

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
    let newItem = {};
    for (let key in item) {
      if (key === "id") {
        newItem.itemId = item[key];
      } else if (key === "name") {
        newItem.itemName = item[key];
      } else if (key === "stock") {
        newItem.initialAvaialableQuantity = item[key];
      } else {
        newItem.key = item[key];
      }
    }
    newItem.currentQunatity = currentQunatity;
    res.json(newItem);
  }
});

app.get("/reserve_product/:itemId", (req, res) => {
  let { itemId } = req.params;
  if (itemId) itemId = parseInt(itemId);
  if (itemId) {
    const requestedItem = getItemById(itemId);
    if (!requestedItem) {
      res.json({ status: "Product not found" });
    }
    if (requestedItem.stock <= 0) {
      res.json({
        status: "Not enough stock available",
        itemId: itemId,
      });
    }
    reserveStockById(itemId, requestedItem.stock);
    res.json({
      status: "Reservation confirmed",
      itemId: itemId,
    });
  }
});

app.listen(1245);
