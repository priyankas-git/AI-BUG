async function fetchUserData(userId) {
  return { id: userId, username: "dev_user" };
}

function displayWelcome(userId) {
  // Bug: Incorrect async handling - referencing promise result as synchronous object without awaiting
  const user = fetchUserData(userId);
  console.log("Welcome " + user.username); // Prints: "Welcome undefined" instead of "Welcome dev_user"
}
