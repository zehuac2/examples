/**
 * @fileoverview Demonstrate the use of prototypes in JavaScript.
 */

function Person(name, age) {
  this.name = name;
  this.age = age;
}

Person.prototype.greet = function () {
  console.log(`Hello, my name is ${this.name} and I am ${this.age} years old.`);
};

function Worker(name, age, job) {
  Person.call(this, name, age);
  this.job = job;
}

Worker.prototype = Object.create(Person.prototype);

Worker.prototype.work = function () {
  console.log(`I am working as a ${this.job}.`);
};

function Other() {}

/**
 * Searching through the prototype chain.
 * @returns {boolean}
 */
function isInstanceOf(obj, cls) {
  let objPrototype = Object.getPrototypeOf(obj);
  const clsPrototype = cls.prototype;

  while (objPrototype) {
    if (objPrototype === clsPrototype) {
      return true;
    }

    objPrototype = Object.getPrototypeOf(objPrototype);
  }

  return false;
}

const person1 = new Person('Alice', 30);
const worker1 = new Worker('Bob', 25, 'Engineer');

person1.greet();
worker1.greet();
worker1.work();

console.log(`Is person1 Person? ${isInstanceOf(person1, Person)}`);
console.log(`Is worker1 Person? ${isInstanceOf(worker1, Person)}`);
console.log(`Is worker1 Other? ${isInstanceOf(worker1, Other)}`);
