function mean_se(root_dir)

fns = dir([ root_dir '/' 'cut_*pred.txt']);

for i = 1:numel(fns)
    fn = fns(i).name;
    data = load(fullfile(root_dir,fn));
    mse = sum((data(:,4) - data(:,2)).^2) / size(data,1);
    rmse = sqrt(mse);
    fprintf('%s, %f, %f\n', fns(i).name, mse, rmse);
    %fprintf('%f, %f\n', mse, rmse);
    
end

end
