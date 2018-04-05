

def optimize(code):
	code_type = type(code)
	if code_type in (tuple, list):
		code = ''.join(code)
	cancels = ['<>', '><', '+-', '-+']
	while(True):
		for c in cancels:
			code = code.replace(c, '')
		break_flag = True
		for c in cancels:
			if c in code:
				break_flag = False
				break
		if break_flag:
			break

	while(code):
		if code[0] == '[':
			idx = 1
			level = 1
			while(True):
				x = code[idx]
				if x == '[':
					level += 1
				elif x == ']':
					level -= 1
					if not level:
						break
				idx += 1
			code = code[idx + 1:]
		else:
			break

	loops = []
	stack = []
	push = stack.append
	pop = stack.pop
	for i, x in enumerate(code):
		if x == '[':
			push(i)
		elif x == ']':
			open_br = pop()
			loops.append((open_br, i))
	loops_to_remove = []
	for loop1 in loops:
		for i, loop2 in enumerate(loops):
			if loop1[1] + 1 == loop2[0]:
				loops_to_remove.append(i)
	code = list(code)
	for i in loops_to_remove:
		loop = loops[i]
		for j in range(loop[0], loop[1] + 1):
			code[j] = ' '
	code = ''.join(code).replace(' ', '')

	return code_type(code)
