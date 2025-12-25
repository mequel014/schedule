{"openapi":"3.1.0","info":{"title":"Duty Schedule API","description":"API for managing doctor duty schedules","version":"1.0.0"},"paths":{"/api/auth/login":{"post":{"tags":["users"],"summary":"Login","operationId":"login_api_auth_login_post","requestBody":{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/LoginRequest"}}},"required":true},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/Token"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/users/me":{"get":{"tags":["users"],"summary":"Get Me","operationId":"get_me_api_users_me_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserWithProfile"}}}}},"security":[{"OAuth2PasswordBearer":[]}]},"patch":{"tags":["users"],"summary":"Update Me","operationId":"update_me_api_users_me_patch","requestBody":{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserUpdate"}}},"required":true},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}},"security":[{"OAuth2PasswordBearer":[]}]}},"/api/users/me/password/change":{"post":{"tags":["users"],"summary":"Change Password","operationId":"change_password_api_users_me_password_change_post","requestBody":{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserPasswordChange"}}},"required":true},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}},"security":[{"OAuth2PasswordBearer":[]}]}},"/api/users":{"get":{"tags":["users"],"summary":"List Users","operationId":"list_users_api_users_get","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"role","in":"query","required":false,"schema":{"$ref":"#/components/schemas/UserRole"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"type":"array","items":{"$ref":"#/components/schemas/UserWithProfile"},"title":"Response List Users Api Users Get"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}},"post":{"tags":["users"],"summary":"Create User","operationId":"create_user_api_users_post","security":[{"OAuth2PasswordBearer":[]}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserCreate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"type":"object","additionalProperties":true,"title":"Response Create User Api Users Post"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/users/{user_id}":{"get":{"tags":["users"],"summary":"Get User","operationId":"get_user_api_users__user_id__get","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"user_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"User Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserWithProfile"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}},"patch":{"tags":["users"],"summary":"Update User","operationId":"update_user_api_users__user_id__patch","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"user_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"User Id"}}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserUpdate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/users/{user_id}/reset-password":{"post":{"tags":["users"],"summary":"Reset Password","operationId":"reset_password_api_users__user_id__reset_password_post","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"user_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"User Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/users/{user_id}/role":{"patch":{"tags":["users"],"summary":"Update User Role","operationId":"update_user_role_api_users__user_id__role_patch","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"user_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"User Id"}}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserRoleUpdate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/UserRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/doctors":{"get":{"tags":["doctors"],"summary":"List Doctors","description":"List all doctors with their current month stats","operationId":"list_doctors_api_doctors_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"items":{"$ref":"#/components/schemas/DoctorWithStats"},"type":"array","title":"Response List Doctors Api Doctors Get"}}}}},"security":[{"OAuth2PasswordBearer":[]}]}},"/api/doctors/me/stats":{"get":{"tags":["doctors"],"summary":"Get My Stats","description":"Get current user's shift statistics","operationId":"get_my_stats_api_doctors_me_stats_get","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"year","in":"query","required":false,"schema":{"type":"integer","title":"Year"}},{"name":"month","in":"query","required":false,"schema":{"type":"integer","title":"Month"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/doctors/me/stats/history":{"get":{"tags":["doctors"],"summary":"Get My Stats History","description":"Get shift statistics history for current user","operationId":"get_my_stats_history_api_doctors_me_stats_history_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}}},"security":[{"OAuth2PasswordBearer":[]}]}},"/api/doctors/{user_id}/profile":{"patch":{"tags":["doctors"],"summary":"Update Doctor Profile","description":"Update doctor's priority and minimum shifts","operationId":"update_doctor_profile_api_doctors__user_id__profile_patch","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"user_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"User Id"}}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/DoctorProfileUpdate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/DoctorProfileRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/schedules":{"get":{"tags":["schedules"],"summary":"List Schedules","description":"List schedules. Doctors only see visible/published ones.","operationId":"list_schedules_api_schedules_get","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"year","in":"query","required":false,"schema":{"type":"integer","title":"Year"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"type":"array","items":{"$ref":"#/components/schemas/ScheduleRead"},"title":"Response List Schedules Api Schedules Get"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}},"post":{"tags":["schedules"],"summary":"Create Schedule","description":"Create or get schedule for month","operationId":"create_schedule_api_schedules_post","security":[{"OAuth2PasswordBearer":[]}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/ScheduleCreate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/ScheduleRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/schedules/current":{"get":{"tags":["schedules"],"summary":"Get Current Schedule","description":"Get current month's schedule as calendar","operationId":"get_current_schedule_api_schedules_current_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/CalendarMonth"}}}}},"security":[{"OAuth2PasswordBearer":[]}]}},"/api/schedules/next":{"get":{"tags":["schedules"],"summary":"Get Next Schedule","description":"Get next month's schedule as calendar","operationId":"get_next_schedule_api_schedules_next_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/CalendarMonth"}}}}},"security":[{"OAuth2PasswordBearer":[]}]}},"/api/schedules/{year}/{month}":{"get":{"tags":["schedules"],"summary":"Get Schedule Calendar","description":"Get schedule for specific month as calendar","operationId":"get_schedule_calendar_api_schedules__year___month__get","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"year","in":"path","required":true,"schema":{"type":"integer","title":"Year"}},{"name":"month","in":"path","required":true,"schema":{"type":"integer","title":"Month"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/CalendarMonth"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/schedules/{schedule_id}":{"patch":{"tags":["schedules"],"summary":"Update Schedule","description":"Update schedule visibility/published status","operationId":"update_schedule_api_schedules__schedule_id__patch","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"schedule_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"Schedule Id"}}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/ScheduleUpdate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/ScheduleRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/schedules/{year}/{month}/generate":{"post":{"tags":["schedules"],"summary":"Auto Generate Schedule","description":"Auto-generate schedule for month","operationId":"auto_generate_schedule_api_schedules__year___month__generate_post","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"year","in":"path","required":true,"schema":{"type":"integer","title":"Year"}},{"name":"month","in":"path","required":true,"schema":{"type":"integer","title":"Month"}},{"name":"seed","in":"query","required":false,"schema":{"type":"integer","description":"Random seed for reproducibility","title":"Seed"},"description":"Random seed for reproducibility"}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/schedules/{schedule_id}/day-settings":{"post":{"tags":["schedules"],"summary":"Set Day Settings","description":"Set custom shift times for a specific day","operationId":"set_day_settings_api_schedules__schedule_id__day_settings_post","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"schedule_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"Schedule Id"}}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/DayShiftSettingsCreate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/DayShiftSettingsRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/schedules/{schedule_id}/shifts":{"post":{"tags":["schedules"],"summary":"Add Shift","description":"Add a shift to schedule","operationId":"add_shift_api_schedules__schedule_id__shifts_post","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"schedule_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"Schedule Id"}}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/ShiftCreate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/ShiftRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/schedules/shifts/{shift_id}":{"patch":{"tags":["schedules"],"summary":"Update Shift","description":"Update a shift","operationId":"update_shift_api_schedules_shifts__shift_id__patch","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"shift_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"Shift Id"}}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/ShiftUpdate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/ShiftRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}},"delete":{"tags":["schedules"],"summary":"Delete Shift","description":"Delete a shift","operationId":"delete_shift_api_schedules_shifts__shift_id__delete","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"shift_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"Shift Id"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/preferences/me":{"get":{"tags":["preferences"],"summary":"Get My Preferences","description":"Get all my preferences grouped by month","operationId":"get_my_preferences_api_preferences_me_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"items":{"$ref":"#/components/schemas/MonthPreferences"},"type":"array","title":"Response Get My Preferences Api Preferences Me Get"}}}}},"security":[{"OAuth2PasswordBearer":[]}]},"post":{"tags":["preferences"],"summary":"Set My Preferences","description":"Set preferences for a month (replaces existing)","operationId":"set_my_preferences_api_preferences_me_post","requestBody":{"content":{"application/json":{"schema":{"$ref":"#/components/schemas/PreferenceCreate"}}},"required":true},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/MonthPreferences"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}},"security":[{"OAuth2PasswordBearer":[]}]}},"/api/preferences/me/{year}/{month}":{"get":{"tags":["preferences"],"summary":"Get My Month Preferences","description":"Get my preferences for a specific month","operationId":"get_my_month_preferences_api_preferences_me__year___month__get","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"year","in":"path","required":true,"schema":{"type":"integer","title":"Year"}},{"name":"month","in":"path","required":true,"schema":{"type":"integer","title":"Month"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/MonthPreferences"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/preferences/me/copy-from-previous":{"post":{"tags":["preferences"],"summary":"Copy From Previous Month","description":"Copy preferences from previous month","operationId":"copy_from_previous_month_api_preferences_me_copy_from_previous_post","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"year","in":"query","required":true,"schema":{"type":"integer","title":"Year"}},{"name":"month","in":"query","required":true,"schema":{"type":"integer","title":"Month"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/swap-requests":{"get":{"tags":["swap-requests"],"summary":"List Swap Requests","description":"List all swap requests (admin only)","operationId":"list_swap_requests_api_swap_requests_get","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"status","in":"query","required":false,"schema":{"$ref":"#/components/schemas/SwapRequestStatus"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"type":"array","items":{"$ref":"#/components/schemas/SwapRequestRead"},"title":"Response List Swap Requests Api Swap Requests Get"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}},"post":{"tags":["swap-requests"],"summary":"Create Swap Request","description":"Create a swap or cancel request","operationId":"create_swap_request_api_swap_requests_post","security":[{"OAuth2PasswordBearer":[]}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/SwapRequestCreate"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/SwapRequestRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/swap-requests/me":{"get":{"tags":["swap-requests"],"summary":"Get My Swap Requests","description":"Get my swap requests","operationId":"get_my_swap_requests_api_swap_requests_me_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"items":{"$ref":"#/components/schemas/SwapRequestRead"},"type":"array","title":"Response Get My Swap Requests Api Swap Requests Me Get"}}}}},"security":[{"OAuth2PasswordBearer":[]}]}},"/api/swap-requests/{request_id}":{"patch":{"tags":["swap-requests"],"summary":"Resolve Swap Request","description":"Approve or reject a swap request","operationId":"resolve_swap_request_api_swap_requests__request_id__patch","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"request_id","in":"path","required":true,"schema":{"type":"string","format":"uuid","title":"Request Id"}}],"requestBody":{"required":true,"content":{"application/json":{"schema":{"$ref":"#/components/schemas/SwapRequestResolve"}}}},"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{"$ref":"#/components/schemas/SwapRequestRead"}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/api/stats/dashboard":{"get":{"tags":["statistics"],"summary":"Get Dashboard","description":"Get dashboard statistics for admins","operationId":"get_dashboard_api_stats_dashboard_get","security":[{"OAuth2PasswordBearer":[]}],"parameters":[{"name":"year","in":"query","required":false,"schema":{"type":"integer","title":"Year"}},{"name":"month","in":"query","required":false,"schema":{"type":"integer","title":"Month"}}],"responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}},"422":{"description":"Validation Error","content":{"application/json":{"schema":{"$ref":"#/components/schemas/HTTPValidationError"}}}}}}},"/health":{"get":{"summary":"Health","operationId":"health_health_get","responses":{"200":{"description":"Successful Response","content":{"application/json":{"schema":{}}}}}}}},"components":{"schemas":{"CalendarMonth":{"properties":{"year":{"type":"integer","title":"Year"},"month":{"type":"integer","title":"Month"},"days":{"items":{"$ref":"#/components/schemas/DayInfo"},"type":"array","title":"Days"},"is_visible":{"type":"boolean","title":"Is Visible"},"is_published":{"type":"boolean","title":"Is Published"}},"type":"object","required":["year","month","days","is_visible","is_published"],"title":"CalendarMonth"},"DayInfo":{"properties":{"date":{"type":"string","format":"date","title":"Date"},"day_of_week":{"type":"integer","title":"Day Of Week"},"is_weekend":{"type":"boolean","title":"Is Weekend"},"is_holiday":{"type":"boolean","title":"Is Holiday"},"default_start_time":{"type":"string","format":"time","title":"Default Start Time"},"default_end_time":{"type":"string","format":"time","title":"Default End Time"},"shifts":{"items":{"$ref":"#/components/schemas/ShiftRead"},"type":"array","title":"Shifts","default":[]},"preferred_doctors":{"items":{"type":"string","format":"uuid"},"type":"array","title":"Preferred Doctors","default":[]}},"type":"object","required":["date","day_of_week","is_weekend","is_holiday","default_start_time","default_end_time"],"title":"DayInfo"},"DayShiftSettingsCreate":{"properties":{"day":{"type":"integer","title":"Day"},"start_time":{"type":"string","format":"time","title":"Start Time"},"end_time":{"type":"string","format":"time","title":"End Time"},"is_holiday":{"type":"boolean","title":"Is Holiday","default":false}},"type":"object","required":["day","start_time","end_time"],"title":"DayShiftSettingsCreate"},"DayShiftSettingsRead":{"properties":{"id":{"type":"string","format":"uuid","title":"Id"},"day":{"type":"integer","title":"Day"},"start_time":{"type":"string","format":"time","title":"Start Time"},"end_time":{"type":"string","format":"time","title":"End Time"},"is_holiday":{"type":"boolean","title":"Is Holiday"}},"type":"object","required":["id","day","start_time","end_time","is_holiday"],"title":"DayShiftSettingsRead"},"DoctorProfileRead":{"properties":{"id":{"type":"string","format":"uuid","title":"Id"},"user_id":{"type":"string","format":"uuid","title":"User Id"},"priority":{"type":"integer","title":"Priority"},"min_shifts_per_month":{"type":"integer","title":"Min Shifts Per Month"}},"type":"object","required":["id","user_id","priority","min_shifts_per_month"],"title":"DoctorProfileRead"},"DoctorProfileUpdate":{"properties":{"priority":{"anyOf":[{"type":"integer"},{"type":"null"}],"title":"Priority"},"min_shifts_per_month":{"anyOf":[{"type":"integer"},{"type":"null"}],"title":"Min Shifts Per Month"}},"type":"object","title":"DoctorProfileUpdate"},"DoctorWithStats":{"properties":{"id":{"type":"string","format":"uuid","title":"Id"},"full_name":{"type":"string","title":"Full Name"},"email":{"type":"string","title":"Email"},"priority":{"type":"integer","title":"Priority"},"min_shifts_per_month":{"type":"integer","title":"Min Shifts Per Month"},"current_month_shifts":{"type":"integer","title":"Current Month Shifts"},"current_month_hours":{"type":"number","title":"Current Month Hours"}},"type":"object","required":["id","full_name","email","priority","min_shifts_per_month","current_month_shifts","current_month_hours"],"title":"DoctorWithStats"},"HTTPValidationError":{"properties":{"detail":{"items":{"$ref":"#/components/schemas/ValidationError"},"type":"array","title":"Detail"}},"type":"object","title":"HTTPValidationError"},"LoginRequest":{"properties":{"email":{"type":"string","format":"email","title":"Email"},"password":{"type":"string","title":"Password"}},"type":"object","required":["email","password"],"title":"LoginRequest"},"MonthPreferences":{"properties":{"year":{"type":"integer","title":"Year"},"month":{"type":"integer","title":"Month"},"days":{"items":{"type":"integer"},"type":"array","title":"Days"}},"type":"object","required":["year","month","days"],"title":"MonthPreferences"},"PreferenceCreate":{"properties":{"year":{"type":"integer","title":"Year"},"month":{"type":"integer","title":"Month"},"days":{"items":{"type":"integer"},"type":"array","title":"Days"}},"type":"object","required":["year","month","days"],"title":"PreferenceCreate"},"ScheduleCreate":{"properties":{"year":{"type":"integer","title":"Year"},"month":{"type":"integer","title":"Month"}},"type":"object","required":["year","month"],"title":"ScheduleCreate"},"ScheduleRead":{"properties":{"id":{"type":"string","format":"uuid","title":"Id"},"year":{"type":"integer","title":"Year"},"month":{"type":"integer","title":"Month"},"is_visible":{"type":"boolean","title":"Is Visible"},"is_published":{"type":"boolean","title":"Is Published"},"shifts":{"items":{"$ref":"#/components/schemas/ShiftRead"},"type":"array","title":"Shifts","default":[]},"day_settings":{"items":{"$ref":"#/components/schemas/DayShiftSettingsRead"},"type":"array","title":"Day Settings","default":[]}},"type":"object","required":["id","year","month","is_visible","is_published"],"title":"ScheduleRead"},"ScheduleUpdate":{"properties":{"is_visible":{"anyOf":[{"type":"boolean"},{"type":"null"}],"title":"Is Visible"},"is_published":{"anyOf":[{"type":"boolean"},{"type":"null"}],"title":"Is Published"}},"type":"object","title":"ScheduleUpdate"},"ShiftCreate":{"properties":{"doctor_id":{"type":"string","format":"uuid","title":"Doctor Id"},"date":{"type":"string","format":"date","title":"Date"},"start_time":{"type":"string","format":"time","title":"Start Time"},"end_time":{"type":"string","format":"time","title":"End Time"}},"type":"object","required":["doctor_id","date","start_time","end_time"],"title":"ShiftCreate"},"ShiftRead":{"properties":{"id":{"type":"string","format":"uuid","title":"Id"},"schedule_id":{"type":"string","format":"uuid","title":"Schedule Id"},"doctor_id":{"type":"string","format":"uuid","title":"Doctor Id"},"date":{"type":"string","format":"date","title":"Date"},"start_time":{"type":"string","format":"time","title":"Start Time"},"end_time":{"type":"string","format":"time","title":"End Time"},"doctor_name":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Doctor Name"}},"type":"object","required":["id","schedule_id","doctor_id","date","start_time","end_time"],"title":"ShiftRead"},"ShiftUpdate":{"properties":{"doctor_id":{"anyOf":[{"type":"string","format":"uuid"},{"type":"null"}],"title":"Doctor Id"},"start_time":{"anyOf":[{"type":"string","format":"time"},{"type":"null"}],"title":"Start Time"},"end_time":{"anyOf":[{"type":"string","format":"time"},{"type":"null"}],"title":"End Time"}},"type":"object","title":"ShiftUpdate"},"SwapRequestCreate":{"properties":{"shift_id":{"type":"string","format":"uuid","title":"Shift Id"},"request_type":{"$ref":"#/components/schemas/SwapRequestType"},"target_doctor_id":{"anyOf":[{"type":"string","format":"uuid"},{"type":"null"}],"title":"Target Doctor Id"},"target_shift_id":{"anyOf":[{"type":"string","format":"uuid"},{"type":"null"}],"title":"Target Shift Id"},"comment":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Comment"}},"type":"object","required":["shift_id","request_type"],"title":"SwapRequestCreate"},"SwapRequestRead":{"properties":{"id":{"type":"string","format":"uuid","title":"Id"},"requester_id":{"type":"string","format":"uuid","title":"Requester Id"},"requester_name":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Requester Name"},"shift_id":{"type":"string","format":"uuid","title":"Shift Id"},"shift_date":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Shift Date"},"request_type":{"$ref":"#/components/schemas/SwapRequestType"},"target_doctor_id":{"anyOf":[{"type":"string","format":"uuid"},{"type":"null"}],"title":"Target Doctor Id"},"target_doctor_name":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Target Doctor Name"},"target_shift_id":{"anyOf":[{"type":"string","format":"uuid"},{"type":"null"}],"title":"Target Shift Id"},"status":{"$ref":"#/components/schemas/SwapRequestStatus"},"comment":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Comment"},"admin_comment":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Admin Comment"},"created_at":{"type":"string","format":"date-time","title":"Created At"},"resolved_at":{"anyOf":[{"type":"string","format":"date-time"},{"type":"null"}],"title":"Resolved At"}},"type":"object","required":["id","requester_id","shift_id","request_type","target_doctor_id","target_shift_id","status","comment","admin_comment","created_at","resolved_at"],"title":"SwapRequestRead"},"SwapRequestResolve":{"properties":{"status":{"$ref":"#/components/schemas/SwapRequestStatus"},"admin_comment":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Admin Comment"}},"type":"object","required":["status"],"title":"SwapRequestResolve"},"SwapRequestStatus":{"type":"string","enum":["pending","approved","rejected"],"title":"SwapRequestStatus"},"SwapRequestType":{"type":"string","enum":["swap","cancel"],"title":"SwapRequestType"},"Token":{"properties":{"access_token":{"type":"string","title":"Access Token"},"token_type":{"type":"string","title":"Token Type","default":"bearer"}},"type":"object","required":["access_token"],"title":"Token"},"UserCreate":{"properties":{"email":{"type":"string","format":"email","title":"Email"},"full_name":{"type":"string","title":"Full Name"},"telegram_username":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Telegram Username"},"role":{"$ref":"#/components/schemas/UserRole","default":"doctor"},"priority":{"type":"integer","title":"Priority","default":1},"min_shifts_per_month":{"type":"integer","title":"Min Shifts Per Month","default":4}},"type":"object","required":["email","full_name"],"title":"UserCreate"},"UserPasswordChange":{"properties":{"old_password":{"type":"string","title":"Old Password"},"new_password":{"type":"string","title":"New Password"}},"type":"object","required":["old_password","new_password"],"title":"UserPasswordChange"},"UserRead":{"properties":{"id":{"type":"string","format":"uuid","title":"Id"},"email":{"type":"string","title":"Email"},"full_name":{"type":"string","title":"Full Name"},"telegram_username":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Telegram Username"},"role":{"$ref":"#/components/schemas/UserRole"},"is_active":{"type":"boolean","title":"Is Active"},"created_at":{"type":"string","format":"date-time","title":"Created At"}},"type":"object","required":["id","email","full_name","telegram_username","role","is_active","created_at"],"title":"UserRead"},"UserRole":{"type":"string","enum":["doctor","admin","sysadmin"],"title":"UserRole"},"UserRoleUpdate":{"properties":{"role":{"$ref":"#/components/schemas/UserRole"}},"type":"object","required":["role"],"title":"UserRoleUpdate"},"UserUpdate":{"properties":{"email":{"anyOf":[{"type":"string","format":"email"},{"type":"null"}],"title":"Email"},"full_name":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Full Name"},"telegram_username":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Telegram Username"},"is_active":{"anyOf":[{"type":"boolean"},{"type":"null"}],"title":"Is Active"}},"type":"object","title":"UserUpdate"},"UserWithProfile":{"properties":{"id":{"type":"string","format":"uuid","title":"Id"},"email":{"type":"string","title":"Email"},"full_name":{"type":"string","title":"Full Name"},"telegram_username":{"anyOf":[{"type":"string"},{"type":"null"}],"title":"Telegram Username"},"role":{"$ref":"#/components/schemas/UserRole"},"is_active":{"type":"boolean","title":"Is Active"},"created_at":{"type":"string","format":"date-time","title":"Created At"},"priority":{"anyOf":[{"type":"integer"},{"type":"null"}],"title":"Priority"},"min_shifts_per_month":{"anyOf":[{"type":"integer"},{"type":"null"}],"title":"Min Shifts Per Month"}},"type":"object","required":["id","email","full_name","telegram_username","role","is_active","created_at"],"title":"UserWithProfile"},"ValidationError":{"properties":{"loc":{"items":{"anyOf":[{"type":"string"},{"type":"integer"}]},"type":"array","title":"Location"},"msg":{"type":"string","title":"Message"},"type":{"type":"string","title":"Error Type"}},"type":"object","required":["loc","msg","type"],"title":"ValidationError"}},"securitySchemes":{"OAuth2PasswordBearer":{"type":"oauth2","flows":{"password":{"scopes":{},"tokenUrl":"/api/auth/login"}}}}}}

Часть 7: Frontend - Configuration
TypeScript

// frontend/nuxt.config.ts

export default defineNuxtConfig({
  future: {
    compatibilityVersion: 4,
  },
  compatibilityDate: '2024-04-03',
  devtools: { enabled: true },
  
  modules: [
    '@pinia/nuxt',
    '@nuxtjs/tailwindcss',
  ],
  
  css: ['~/assets/css/main.css'],
  
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000'
    }
  },
  
  app: {
    head: {
      title: 'Расписание дежурств',
      meta: [
        { name: 'description', content: 'Система управления расписанием дежурных врачей' }
      ]
    }
  }
})
JavaScript

// frontend/tailwind.config.js

module.exports = {
  content: [
    './app/components/**/*.{vue,js}',
    './app/layouts/**/*.vue',
    './app/pages/**/*.vue',
    './app/plugins/**/*.{js,ts}',
    './app/app.vue',
  ],
  theme: {
    extend: {},
  },
  plugins: [require('daisyui')],
  daisyui: {
    themes: ['light', 'dark'],
  },
}
CSS

/* frontend/app/assets/css/main.css */

@tailwind base;
@tailwind components;
@tailwind utilities;

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 0.25rem;
}

.day-cell {
  @apply border rounded-lg p-2 min-h-[100px] transition-all;
}

.day-cell:hover {
  @apply shadow-md;
}

.day-cell.weekend {
  @apply bg-orange-50;
}

.day-cell.holiday {
  @apply bg-red-50;
}

.doctor-card {
  @apply px-2 py-1 rounded text-sm cursor-move;
}

.doctor-card.dragging {
  @apply opacity-50;
}
Часть 8: Frontend - Plugins & Stores
JavaScript

// frontend/app/plugins/api.js

export default defineNuxtPlugin(() => {
  const config = useRuntimeConfig()
  const authStore = useAuthStore()

  const $api = async (url, options = {}) => {
    const headers = { ...options.headers }
    
    if (authStore.token) {
      headers.Authorization = `Bearer ${authStore.token}`
    }
    
    if (!(options.body instanceof FormData)) {
      headers['Content-Type'] = 'application/json'
    }

    const response = await $fetch(`${config.public.apiBase}${url}`, {
      ...options,
      headers,
    })
    
    return response
  }

  return {
    provide: {
      api: $api
    }
  }
})
JavaScript

// frontend/app/stores/auth.js

export const useAuthStore = defineStore('auth', () => {
  const token = ref(null)
  const user = ref(null)
  const loading = ref(false)

  // Load token from localStorage on init
  if (process.client) {
    token.value = localStorage.getItem('auth_token')
  }

  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => user.value?.role === 'admin' || user.value?.role === 'sysadmin')
  const isSysadmin = computed(() => user.value?.role === 'sysadmin')
  const isDoctor = computed(() => user.value?.role === 'doctor' || user.value?.role === 'sysadmin')

  async function login(email, password) {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const response = await $api('/api/auth/login', {
        method: 'POST',
        body: { email, password }
      })
      token.value = response.access_token
      if (process.client) {
        localStorage.setItem('auth_token', response.access_token)
      }
      await fetchUser()
      return true
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  async function fetchUser() {
    if (!token.value) return null
    const { $api } = useNuxtApp()
    try {
      user.value = await $api('/api/users/me')
      return user.value
    } catch (error) {
      logout()
      throw error
    }
  }

  function logout() {
    token.value = null
    user.value = null
    if (process.client) {
      localStorage.removeItem('auth_token')
    }
    navigateTo('/login')
  }

  async function changePassword(oldPassword, newPassword) {
    const { $api } = useNuxtApp()
    await $api('/api/users/me/password/change', {
      method: 'POST',
      body: { old_password: oldPassword, new_password: newPassword }
    })
  }

  return {
    token,
    user,
    loading,
    isAuthenticated,
    isAdmin,
    isSysadmin,
    isDoctor,
    login,
    logout,
    fetchUser,
    changePassword
  }
})
JavaScript

// frontend/app/stores/schedule.js

export const useScheduleStore = defineStore('schedule', () => {
  const currentSchedule = ref(null)
  const nextSchedule = ref(null)
  const loading = ref(false)
  const selectedMonth = ref({ year: null, month: null })

  async function fetchCurrentSchedule() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      currentSchedule.value = await $api('/api/schedules/current')
      return currentSchedule.value
    } finally {
      loading.value = false
    }
  }

  async function fetchNextSchedule() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      nextSchedule.value = await $api('/api/schedules/next')
      return nextSchedule.value
    } finally {
      loading.value = false
    }
  }

  async function fetchSchedule(year, month) {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const schedule = await $api(`/api/schedules/${year}/${month}`)
      selectedMonth.value = { year, month }
      return schedule
    } finally {
      loading.value = false
    }
  }

  async function generateSchedule(year, month, seed = null) {
    const { $api } = useNuxtApp()
    const url = seed 
      ? `/api/schedules/${year}/${month}/generate?seed=${seed}`
      : `/api/schedules/${year}/${month}/generate`
    return await $api(url, { method: 'POST' })
  }

  async function updateScheduleVisibility(scheduleId, isVisible, isPublished) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/${scheduleId}`, {
      method: 'PATCH',
      body: { is_visible: isVisible, is_published: isPublished }
    })
  }

  async function addShift(scheduleId, shiftData) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/${scheduleId}/shifts`, {
      method: 'POST',
      body: shiftData
    })
  }

  async function updateShift(shiftId, data) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/shifts/${shiftId}`, {
      method: 'PATCH',
      body: data
    })
  }

  async function deleteShift(shiftId) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/shifts/${shiftId}`, {
      method: 'DELETE'
    })
  }

  async function setDaySettings(scheduleId, dayData) {
    const { $api } = useNuxtApp()
    return await $api(`/api/schedules/${scheduleId}/day-settings`, {
      method: 'POST',
      body: dayData
    })
  }

  return {
    currentSchedule,
    nextSchedule,
    loading,
    selectedMonth,
    fetchCurrentSchedule,
    fetchNextSchedule,
    fetchSchedule,
    generateSchedule,
    updateScheduleVisibility,
    addShift,
    updateShift,
    deleteShift,
    setDaySettings
  }
})
JavaScript

// frontend/app/stores/doctors.js

export const useDoctorsStore = defineStore('doctors', () => {
  const doctors = ref([])
  const loading = ref(false)

  async function fetchDoctors() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      doctors.value = await $api('/api/doctors')
      return doctors.value
    } finally {
      loading.value = false
    }
  }

  async function updateDoctorProfile(userId, data) {
    const { $api } = useNuxtApp()
    const updated = await $api(`/api/doctors/${userId}/profile`, {
      method: 'PATCH',
      body: data
    })
    // Update local state
    const idx = doctors.value.findIndex(d => d.id === userId)
    if (idx !== -1) {
      doctors.value[idx] = { ...doctors.value[idx], ...data }
    }
    return updated
  }

  async function fetchMyStats(year, month) {
    const { $api } = useNuxtApp()
    const params = new URLSearchParams()
    if (year) params.set('year', year)
    if (month) params.set('month', month)
    return await $api(`/api/doctors/me/stats?${params.toString()}`)
  }

  async function fetchMyStatsHistory() {
    const { $api } = useNuxtApp()
    return await $api('/api/doctors/me/stats/history')
  }

  return {
    doctors,
    loading,
    fetchDoctors,
    updateDoctorProfile,
    fetchMyStats,
    fetchMyStatsHistory
  }
})
JavaScript

// frontend/app/stores/preferences.js

export const usePreferencesStore = defineStore('preferences', () => {
  const myPreferences = ref([])
  const loading = ref(false)

  async function fetchMyPreferences() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      myPreferences.value = await $api('/api/preferences/me')
      return myPreferences.value
    } finally {
      loading.value = false
    }
  }

  async function fetchMonthPreferences(year, month) {
    const { $api } = useNuxtApp()
    return await $api(`/api/preferences/me/${year}/${month}`)
  }

  async function setPreferences(year, month, days) {
    const { $api } = useNuxtApp()
    const result = await $api('/api/preferences/me', {
      method: 'POST',
      body: { year, month, days }
    })
    await fetchMyPreferences()
    return result
  }

  async function copyFromPrevious(year, month) {
    const { $api } = useNuxtApp()
    const result = await $api(`/api/preferences/me/copy-from-previous?year=${year}&month=${month}`, {
      method: 'POST'
    })
    await fetchMyPreferences()
    return result
  }

  return {
    myPreferences,
    loading,
    fetchMyPreferences,
    fetchMonthPreferences,
    setPreferences,
    copyFromPrevious
  }
})
JavaScript

// frontend/app/stores/users.js

export const useUsersStore = defineStore('users', () => {
  const users = ref([])
  const loading = ref(false)

  async function fetchUsers(role = null) {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const params = role ? `?role=${role}` : ''
      users.value = await $api(`/api/users${params}`)
      return users.value
    } finally {
      loading.value = false
    }
  }

  async function createUser(userData) {
    const { $api } = useNuxtApp()
    const result = await $api('/api/users', {
      method: 'POST',
      body: userData
    })
    await fetchUsers()
    return result
  }

  async function updateUser(userId, data) {
    const { $api } = useNuxtApp()
    const updated = await $api(`/api/users/${userId}`, {
      method: 'PATCH',
      body: data
    })
    const idx = users.value.findIndex(u => u.id === userId)
    if (idx !== -1) {
      users.value[idx] = updated
    }
    return updated
  }

  async function updateUserRole(userId, role) {
    const { $api } = useNuxtApp()
    return await $api(`/api/users/${userId}/role`, {
      method: 'PATCH',
      body: { role }
    })
  }

  async function resetUserPassword(userId) {
    const { $api } = useNuxtApp()
    return await $api(`/api/users/${userId}/reset-password`, {
      method: 'POST'
    })
  }

  return {
    users,
    loading,
    fetchUsers,
    createUser,
    updateUser,
    updateUserRole,
    resetUserPassword
  }
})
JavaScript

// frontend/app/stores/swapRequests.js

export const useSwapRequestsStore = defineStore('swapRequests', () => {
  const requests = ref([])
  const myRequests = ref([])
  const loading = ref(false)

  async function fetchRequests(status = null) {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      const params = status ? `?status=${status}` : ''
      requests.value = await $api(`/api/swap-requests${params}`)
      return requests.value
    } finally {
      loading.value = false
    }
  }

  async function fetchMyRequests() {
    const { $api } = useNuxtApp()
    loading.value = true
    try {
      myRequests.value = await $api('/api/swap-requests/me')
      return myRequests.value
    } finally {
      loading.value = false
    }
  }

  async function createRequest(data) {
    const { $api } = useNuxtApp()
    const result = await $api('/api/swap-requests', {
      method: 'POST',
      body: data
    })
    await fetchMyRequests()
    return result
  }

  async function resolveRequest(requestId, status, adminComment = null) {
    const { $api } = useNuxtApp()
    const result = await $api(`/api/swap-requests/${requestId}`, {
      method: 'PATCH',
      body: { status, admin_comment: adminComment }
    })
    await fetchRequests()
    return result
  }

  const pendingCount = computed(() => 
    requests.value.filter(r => r.status === 'pending').length
  )

  return {
    requests,
    myRequests,
    loading,
    pendingCount,
    fetchRequests,
    fetchMyRequests,
    createRequest,
    resolveRequest
  }
})
Часть 9: Frontend - Middleware & Utils
JavaScript

// frontend/app/middleware/auth.js

export default defineNuxtRouteMiddleware(async (to) => {
  const authStore = useAuthStore()
  
  // Skip for login page
  if (to.path === '/login') {
    return
  }
  
  // Check if authenticated
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  
  // Fetch user if not loaded
  if (!authStore.user) {
    try {
      await authStore.fetchUser()
    } catch (error) {
      return navigateTo('/login')
    }
  }
})
JavaScript

// frontend/app/middleware/admin.js

export default defineNuxtRouteMiddleware(async () => {
  const authStore = useAuthStore()
  
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  
  if (!authStore.user) {
    await authStore.fetchUser()
  }
  
  if (!authStore.isAdmin) {
    return navigateTo('/doctor')
  }
})
JavaScript

// frontend/app/middleware/sysadmin.js

export default defineNuxtRouteMiddleware(async () => {
  const authStore = useAuthStore()
  
  if (!authStore.isAuthenticated) {
    return navigateTo('/login')
  }
  
  if (!authStore.user) {
    await authStore.fetchUser()
  }
  
  if (!authStore.isSysadmin) {
    return navigateTo('/admin')
  }
})
JavaScript

// frontend/app/utils/dateHelpers.js

export const MONTH_NAMES = [
  'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
  'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
]

export const WEEKDAY_NAMES = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

export const WEEKDAY_FULL = [
  'Понедельник', 'Вторник', 'Среда', 'Четверг', 
  'Пятница', 'Суббота', 'Воскресенье'
]

export function formatDate(date) {
  if (typeof date === 'string') {
    date = new Date(date)
  }
  return date.toLocaleDateString('ru-RU')
}

export function formatTime(time) {
  if (!time) return ''
  if (typeof time === 'string') {
    return time.substring(0, 5)
  }
  return time
}

export function getNextMonth(year, month) {
  if (month === 12) {
    return { year: year + 1, month: 1 }
  }
  return { year, month: month + 1 }
}

export function getPrevMonth(year, month) {
  if (month === 1) {
    return { year: year - 1, month: 12 }
  }
  return { year, month: month - 1 }
}

export function getDaysInMonth(year, month) {
  return new Date(year, month, 0).getDate()
}

export function getFirstDayOfMonth(year, month) {
  // Returns 0-6 (Mon=0, Sun=6) to match our calendar
  const day = new Date(year, month - 1, 1).getDay()
  return day === 0 ? 6 : day - 1
}
JavaScript

// frontend/app/utils/shiftHelpers.js

export function calculateShiftHours(startTime, endTime) {
  const [startH, startM] = startTime.split(':').map(Number)
  const [endH, endM] = endTime.split(':').map(Number)
  
  let hours
  if (endH <= startH && !(endH === startH && endM > startM)) {
    // Next day
    hours = (24 - startH - startM / 60) + (endH + endM / 60)
  } else {
    hours = (endH + endM / 60) - (startH + startM / 60)
  }
  
  return Math.round(hours * 10) / 10
}

export function isNextDay(startTime, endTime) {
  const [startH] = startTime.split(':').map(Number)
  const [endH] = endTime.split(':').map(Number)
  return endH <= startH
}

export function formatShiftTime(startTime, endTime) {
  const start = startTime.substring(0, 5)
  const end = endTime.substring(0, 5)
  const next = isNextDay(startTime, endTime) ? ' (+1)' : ''
  return `${start} - ${end}${next}`
}
JavaScript

// frontend/app/composables/useDragDrop.js

export function useDragDrop() {
  const draggingDoctor = ref(null)
  const dragOverDate = ref(null)

  function handleDragStart(doctor, event) {
    draggingDoctor.value = doctor
    event.dataTransfer.effectAllowed = 'move'
    event.dataTransfer.setData('text/plain', doctor.id)
  }

  function handleDragEnd() {
    draggingDoctor.value = null
    dragOverDate.value = null
  }

  function handleDragOver(date, event) {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'move'
    dragOverDate.value = date
  }

  function handleDragLeave() {
    dragOverDate.value = null
  }

  return {
    draggingDoctor,
    dragOverDate,
    handleDragStart,
    handleDragEnd,
    handleDragOver,
    handleDragLeave
  }
}
Часть 10: Frontend - Layouts
vue

<!-- frontend/app/layouts/default.vue -->
<script setup>
const authStore = useAuthStore()

onMounted(async () => {
  if (authStore.isAuthenticated && !authStore.user) {
    await authStore.fetchUser()
  }
})
</script>

<template>
  <div class="min-h-screen bg-base-200">
    <UiNavbar />
    <main class="container mx-auto px-4 py-6">
      <slot />
    </main>
  </div>
</template>
vue

<!-- frontend/app/layouts/admin.vue -->
<script setup>
definePageMeta({
  middleware: ['auth', 'admin']
})

const authStore = useAuthStore()
const swapRequestsStore = useSwapRequestsStore()

onMounted(async () => {
  if (authStore.isAuthenticated) {
    await swapRequestsStore.fetchRequests('pending')
  }
})
</script>

<template>
  <div class="min-h-screen bg-base-200">
    <UiNavbar />
    <div class="flex">
      <AdminSidebar />
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
vue

<!-- frontend/app/layouts/doctor.vue -->
<script setup>
definePageMeta({
  middleware: ['auth']
})

const authStore = useAuthStore()
</script>

<template>
  <div class="min-h-screen bg-base-200">
    <UiNavbar />
    <div class="flex">
      <DoctorSidebar />
      <main class="flex-1 p-6">
        <slot />
      </main>
    </div>
  </div>
</template>
Часть 11: Frontend - UI Components
vue

<!-- frontend/app/components/Ui/Navbar.vue -->
продолжи отсюда