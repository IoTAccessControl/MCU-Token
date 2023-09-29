#ifndef __PWM_H_
#define	__PWM_H_

void fp_pwm_init(int clock_source_number, int duty, int frequency, int duty_resolution, int timer, int channel);
void fp_pwm_stop(void);

#endif /* __PWM_H_ */
