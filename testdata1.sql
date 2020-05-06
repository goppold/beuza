DELETE FROM votes;
DELETE FROM cycles;
ALTER SEQUENCE cycles_cycle_id_seq RESTART WITH 1;
DELETE FROM users;
ALTER SEQUENCE users_user_id_seq RESTART WITH 1;
DELETE FROM events;
ALTER SEQUENCE events_event_id_seq RESTART WITH 1;
DELETE FROM devices;
ALTER SEQUENCE devices_device_id_seq RESTART WITH 1;

INSERT INTO devices (unique_identifier,count_of_wins,count_of_events) VALUES ('sepp_handy','2','10');
INSERT INTO devices (unique_identifier,count_of_wins,count_of_events) VALUES ('sebi_handy','3','10');
INSERT INTO devices (unique_identifier,count_of_wins,count_of_events) VALUES ('hias_handy','0','10');
INSERT INTO devices (unique_identifier,count_of_wins,count_of_events) VALUES ('flo_handy','99','100');
INSERT INTO devices (unique_identifier,count_of_wins,count_of_events) VALUES ('kw_handy','3','25');

INSERT INTO events (name,invitation_key,owner_device_id) VALUES ('Prag','abc12','1');
INSERT INTO events (name,invitation_key,owner_device_id) VALUES ('Berlin','cde23','3');
INSERT INTO events (name,invitation_key,owner_device_id) VALUES ('Pjöngjang','def34','2');

INSERT INTO users (device_id,name,is_admin,event_id,is_active) VALUES ('1','Sepp',TRUE,'1',FALSE);
INSERT INTO users (device_id,name,is_admin,event_id,is_active) VALUES ('2','Sebi',TRUE,'1',TRUE);
INSERT INTO users (device_id,name,is_admin,event_id,is_active) VALUES ('3','Hias',FALSE,'1',TRUE);
INSERT INTO users (device_id,name,is_admin,event_id,is_active) VALUES ('5','KW',FALSE,'1',TRUE);
INSERT INTO users (device_id,name,is_admin,event_id,is_active) VALUES ('2','Weizenninja',TRUE,'2',TRUE);
INSERT INTO users (device_id,name,is_admin,event_id,is_active) VALUES ('4','WonderwallFlo',FALSE,'2',TRUE);
INSERT INTO users (device_id,name,is_admin,event_id,is_active) VALUES ('1','Vorstand',FALSE,'3',TRUE);
INSERT INTO users (device_id,name,is_admin,event_id,is_active) VALUES ('2','I bims',TRUE,'3',TRUE);

INSERT INTO cycles (state,end_date_time,event_id) VALUES ('betting',date '2019-01-01' + time '13:37:30.085337','1');
INSERT INTO cycles (state,end_date_time,event_id) VALUES ('closed',date '2019-01-02' + time '13:07:30.085337','1');
INSERT INTO cycles (state,end_date_time,event_id) VALUES ('voting',date '2019-01-03' + time '14:37:30.085337','1');
INSERT INTO cycles (state,end_date_time,event_id) VALUES ('betting',date '2019-01-04' + time '00:17:30.085337','1');
INSERT INTO cycles (state,end_date_time,event_id) VALUES ('betting',date '2020-01-01' + time '23:37:30.085337','2');
INSERT INTO cycles (state,end_date_time,event_id) VALUES ('closed',date '2020-01-02' + time '13:37:30.085337','2');
INSERT INTO cycles (state,end_date_time,event_id) VALUES ('betting',date '2020-01-01' + time '13:37:30.085337','3');

INSERT INTO polls (user_id,cycle_id,voted_user_id) VALUES ('1','1','4');
INSERT INTO polls (user_id,cycle_id,voted_user_id) VALUES ('2','1','4');
INSERT INTO polls (user_id,cycle_id,voted_user_id) VALUES ('3','1','1');
INSERT INTO polls (user_id,cycle_id,voted_user_id) VALUES ('1','3','2');
INSERT INTO polls (user_id,cycle_id,voted_user_id) VALUES ('2','3','1');
INSERT INTO polls (user_id,cycle_id,voted_user_id) VALUES ('3','3','2');
INSERT INTO polls (user_id,cycle_id,voted_user_id) VALUES ('4','3','2');
INSERT INTO polls (user_id,cycle_id,voted_user_id) VALUES ('8','7','8');
