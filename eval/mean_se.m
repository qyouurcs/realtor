fns = dir('./cut_*pred.txt');

for i = 1:numel(fns)
    fn = fns(i).name;
    data = load(fn);
    mse = sum((data(:,3) - data(:,2)).^2) / size(data,1);
    rmse = sqrt(mse);
    %fprintf('%s, %f, %f\n', fns(i).name, mse, rmse);
    fprintf('%f, %f\n', mse, rmse);
    
end