async function getCategories() {
  const response = await fetch("/api/v1/categories")
  const categories = await response.json()
  for (const category of categories) {
    const cat = document.createElement("option")
    cat.value = category.id
    cat.textContent = category.name
    document.getElementById("categoryId").appendChild(cat)
  }
}

async function openItem(itemId) {
  await fetch(`/api/v1/fridge/${itemId}`, { method: "PATCH" })
  getItems()
}

async function deleteItem(itemId) {
  await fetch(`/api/v1/fridge/${itemId}`, { method: "DELETE" })
  getItems()
}

async function getItems() {
  document.getElementById("itemList").innerHTML = "" //pulisco itemList
  const params = new URLSearchParams()
  if (document.getElementById("owner").value) params.append("ownedBy", document.getElementById("owner").value)
  if (document.getElementById("expireDays").value) params.append("expiresIn", document.getElementById("expireDays").value)

  const response = await fetch(`/api/v1/fridge?${params}`);
  const items = await response.json();

  for (const item of items) {
    const itemEntry = document.createElement("li")
    itemEntry.textContent = `${item.name}, ${item.amount} ${item.unit}. Owned By ${item.ownedBy} and expires ${item.expDate}`

    if (!item.openedAt) {
      const openButton = document.createElement("button")
      openButton.textContent = "Open"
      openButton.onclick = () => openItem(item.id)
      itemEntry.appendChild(openButton)
    }
    const deleteButton = document.createElement("button")
    deleteButton.textContent = "Delete"
    deleteButton.onclick = () => deleteItem(item.id)
    itemEntry.appendChild(deleteButton)
    
    document.getElementById("itemList").appendChild(itemEntry)
  }  
}

document.getElementById("itemForm").addEventListener("submit", async event => {
  event.preventDefault()
  const query = {
    name: document.getElementById("name").value,
    ownedBy: document.getElementById("ownedBy").value,
    categoryId: Number(document.getElementById("categoryId").value),
    amount: Number(document.getElementById("amount").value) || null,
    unit: document.getElementById("unit").value || null,
    expDate: document.getElementById("expDate").value || null
  }
  await fetch("/api/v1/fridge", { method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(query) })
  document.getElementById("itemForm").reset()
  getItems()
})

document.getElementById("searchButton").onclick = getItems
getCategories()
getItems()