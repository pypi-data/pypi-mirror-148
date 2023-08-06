
##### PyQueue
##### A simple module lib to queue your lists!
**_Usage:_**
-
```py
# List: The list you are going to transform into a queue
# Length: The maximum size of the queue
# Input: The input from the user (can be a input('')) or an str

Queue(list, length, input)
# Returns the simple queue

Queue(list, length, input).input()
# Returns the element that was added

Queue(list, length, input).output()
# Returns the element that was removed

Queue(list, length, input).infos() # or .info()
# Returns the queue, the input and the output of the queue.
```

**_How it works_**
-
- Insert the wanted string onto the list if the maximum size of the list is less than the wanted size.
- If the size of the list is greater than the wanted size, pop out the last queue element and insert the wanted string.
---
### _TODO_:
- [ ] Add `.create()` function
	- will create 2 buffers for temporary usage.
	- e.g: `Queue(q, 3, in).create(1)`
		- creates a new buffer **inside** the **`Queue`** _class_ itself
		- can use `.input()`, `.output()` and `.infos()`
		- cannot be referenced outside the **`Queue`** _class_.
- [ ] Double-Reference `return` Methods
	- allows the user to reference `Queue` without needing to `print()` it. 
		- also allows the user to reference `Queue` with `print()`.
---
```mermaid
graph TD
    A[Read the input] -->|Verify if the size is less than the wanted|B(Insert string on the first position)
    B --> C{Check the queue}
    C -->|If the size is less|D[Insert at 0 and move the rest]
    C -->|If size is greater|E[Insert at 0 and pop the last]
    E --> F
    D --> F
    F{Rest of args}
    F --> |.input|H(print the new element)
    F --> |.output|G(print the removed element)
    F --> |info / infos|I(print the queue, the input and the output)
```


