beginfig(1)
	u = 5mm;

	for i = 0 upto 2:
		for j = 0 upto 2:
			draw 
				((i + 0) * u, (j + 0) * u) --
				((i + 1) * u, (j + 0) * u) --
				((i + 1) * u, (j + 1) * u) --
				((i + 0) * u, (j + 1) * u) --
				cycle;
		
		endfor;
	endfor;

  	fill fullcircle scaled 0.3u shifted (0.5u, 2.5u);

	drawarrow (0.5u, 2.5u) -- (1.5u, 0.5u);
	drawarrow (0.5u, 2.5u) -- (2.5u, 1.5u);
	
endfig;

end;
