const array = new Proxy([], {
  get(target, prop) {
    if (Number.isInteger(Number(prop))) {
      console.log(`Accessing index ${prop}`);
    }

    return target[prop];
  },
  set(target, prop, value) {
    if (prop === 'length') {
      target[prop] = value;
      return true;
    }
    console.log(`Added new element to array: ${value}`);
    target[prop] = value;

    return true;
  },
});

array.push(11);
array.push(22);

console.log(array[0]);
console.log(array[1]);
