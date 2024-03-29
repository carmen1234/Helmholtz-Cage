M = csvread("sensor_data.csv", 1, 0);

magnetic_field = M(:, 4:6);

target_mag = zeros(size(magnetic_field));
target_mag(:, 1) = 1;
target_mag(:, 2) = 1;
target_mag(:, 3) = 1;

diff = (target_mag-magnetic_field).^2;

mse_x= mean(mean(diff(:,1),2),1);
mse_y= mean(mean(diff(:,2),2),1);
mse_z= mean(mean(diff(:,3),2),1);

%-------------------------

max_x = max(magnetic_field(:,1));
max_y = max(magnetic_field(:,2));
max_z = max(magnetic_field(:,3));

min_x = min(magnetic_field(:,1));
min_y = min(magnetic_field(:,2));
min_z = min(magnetic_field(:,3));

target_x = target_mag(1,1);
target_y = target_mag(1,2);
target_z = target_mag(1,3);

x_error1 = abs(max_x/target_x)*100;
x_error2 = abs(min_x/target_x)*100;

y_error1 = abs(max_y/target_y)*100;
y_error2 = abs(min_y/target_y)*100;

z_error1 = abs(max_z/target_z)*100;
z_error2 = abs(min_z/target_z)*100;

if (abs(100-x_error1) > 5 || abs(100-x_error1) > 5)
    "Greater than 5% error"
end


