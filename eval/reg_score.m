fns = dir('./cut_*pred.txt');

for i = 1:numel(fns)
    fn = fns(i).name;
    data = load(fn);
    mse = sum((data(:,4) - data(:,2)).^2);
    mse_t = sum(( data(:,2) - mean( data(:,2))).^2);
    fprintf('%s, %f\n', fn, 1 - ( mse / mse_t));
end