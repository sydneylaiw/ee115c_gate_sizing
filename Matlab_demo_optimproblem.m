%% TA reference code

Cin = 3;
g1 = 4/3; p1 = 2; g2 = 1; p2 = 1; Cload1 = 150;
g3 = 5/3; p3 = 2; g4 = 1; p4 = 1; Cload2 = 75;

%% initialize the optimization 
% optimvar('variableName', dim1, dim2, 'var', var key)
x = optimvar('x', 4, 1,'LowerBound', 1);
prob = optimproblem('ObjectiveSense', 'minimize');

%setup the optimization objective: Minimize the delay 
prob.Objective = (x(1) + x(3))/Cin + 1 + x(2)/x(1) * g1 + p1 + Cload1 / x(2) * g2 + p2;


% optimization constraint 1: the delays of all paths are same
prob.Constraints.delays = x(2)/x(1) * g1 + p1 + Cload1 / x(2) * g2 + p2 ...
                        == x(4)/x(3) * g3 + p3 + Cload2 / x(4) * g4 + p4;


x0.x = 2 * ones(4,1);

sol = solve(prob, x0);
