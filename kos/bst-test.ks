function PID_init {
    declare parameter
        Kp,
        Ki,
        Kd,
        t_min,  // minimum of throttle range
        t_max.  // maximum of throttle range

    local P is 0.           // Proportion
    local I is 0.           // Integral    -->   summation
    local D is 0.           // Derivative  -->   difference
    local old_t is -1.      // previous time point (init with -1)
    local old_input is 0.   // previous return value of PID controller

    local PID_array is list(Kp, Ki, Kd, t_min, t_max,
                            P, I, D, old_t, old_input).

    return PID_array.
}.


function PID {
    declare parameter
        PID_array,  // array init with PID_init
        seek_val,   // value we want
        cur_val.    // value we currently have

    local Kp        is PID_array[0].
    local Ki        is PID_array[1].
    local Kd        is PID_array[2].
    local t_min     is PID_array[3].
    local t_max     is PID_array[4].
    local old_P     is PID_array[5].
    local old_I     is PID_array[6].
    local old_D     is PID_array[7].
    local old_t     is PID_array[8].
    local old_input is PID_array[9].

    local P         is seek_val - cur_val.
    local I         is old_I.
    local D         is old_D.
    local new_input is old_input.

    local t is time:seconds.
    local dt is t - old_t.

    if dt>0{
                set D to (P - old_P) / dt.
                local only_pd is Kp * P + Kd  * D.
                if (old_I > 0 or only_pd > t_min) and (old_I < 0 or only_pd < t_max) {
                        set I to old_I + P * dt.
                }.
                set new_input to only_pd + Ki * I.
        }
        set new_input to max(t_min, min(t_max, new_input)).

    set PID_array[5] to P.
    set PID_array[6] to I.
    set PID_array[7] to D.
    set PID_array[8] to t.
    set PID_array[9] to new_input.

    return new_input.
}.

clearscreen.
print "autolanding started.".
local gear_flag is 0.
set target_alt to 0.
AG9 on.
gear off.
sas off.
rcs on.
lock steering to srfRetrograde.
set PID_param to PID_init(0.2, 0.0, 0.6, 0, 1).
wait until alt:radar < 25000.
print"ignition point 1 :(25000,0.33,1300).".
lock throttle to 0.33.
until FALSE{
        if ship:velocity:surface:mag < 1300{
            lock throttle to 0.
            print"ignition point 1 ended.".
            break.
        }
}
wait until alt:radar < 5000.
print"ignition point 2 :(5000,0.8,50).".
lock throttle to 0.8.
until FALSE{
        if ship:velocity:surface:mag < 50{
            lock throttle to 0.
            print"ignition point 2 ended.".
            break.
        }
}
wait until alt:radar < 1500.
print"PID control started.".
until FALSE{
    if gear_flag = 0 and alt:radar < 400{ 
        gear on.
        set gear_flag to 1.
    }
    set current_alt to alt:radar.
    set throttle_rate to PID(PID_param, target_alt, current_alt).
    lock throttle to throttle_rate.
    print "altitude(btm):"+round(current_alt,2) at (20,10).
    print "        delta:"+round(current_alt - target_alt,2) at (20,11).
    print "throttle rate:"+round(throttle_rate,2) at (20,12).
    if (ship:groundspeed >-2 and alt:radar <45){
        lock throttle to 0.
        print "v & h fit the settings, PID ended.".
        break.
    }
}
rcs off.
lock throttle to 0.
print "autolanding completed.".
// run"0:/bst-test.ks".
