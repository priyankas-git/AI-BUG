function getPostalCode(user) {
  // Bug: Null/undefined property access on nested objects
  return user.address.postalCode; 
}

console.log(getPostalCode({ name: "John" })); // Error: Cannot read properties of undefined (reading 'postalCode')
