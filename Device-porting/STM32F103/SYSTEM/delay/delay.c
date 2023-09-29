#include "delay.h"
#include "sys.h"

#if SYSTEM_SUPPORT_OS
#include "includes.h"
#endif

static u32 fac_us=0;

#if SYSTEM_SUPPORT_OS		
    static u16 fac_ms=0;
#endif
	
#if SYSTEM_SUPPORT_OS
#ifdef 	OS_CRITICAL_METHOD	
#define delay_osrunning		OSRunning
#define delay_ostickspersec	OS_TICKS_PER_SEC
#define delay_osintnesting 	OSIntNesting
#endif

#ifdef 	CPU_CFG_CRITICAL_METHOD
#define delay_osrunning		OSRunning
#define delay_ostickspersec	OSCfg_TickRate_Hz
#define delay_osintnesting 	OSIntNestingCtr
#endif

void delay_osschedlock(void)
{
#ifdef CPU_CFG_CRITICAL_METHOD
	OS_ERR err; 
	OSSchedLock(&err);
#else
	OSSchedLock();
#endif
}

void delay_osschedunlock(void)
{	
#ifdef CPU_CFG_CRITICAL_METHOD
	OS_ERR err; 
	OSSchedUnlock(&err);
#else
	OSSchedUnlock();		
#endif
}

void delay_ostimedly(u32 ticks)
{
#ifdef CPU_CFG_CRITICAL_METHOD
	OS_ERR err; 
	OSTimeDly(ticks,OS_OPT_TIME_PERIODIC,&err);
#else
	OSTimeDly(ticks);
#endif 
}
 
void SysTick_Handler(void)
{	
	if(delay_osrunning==1)
	{
		OSIntEnter();
		OSTimeTick();
		OSIntExit();
	}
}
#endif

void delay_init(u8 SYSCLK)
{
#if SYSTEM_SUPPORT_OS
	u32 reload;
#endif
    HAL_SYSTICK_CLKSourceConfig(SYSTICK_CLKSOURCE_HCLK);
	fac_us=SYSCLK;
#if SYSTEM_SUPPORT_OS
	reload=SYSCLK;   
	reload*=1000000/delay_ostickspersec;
	fac_ms=1000/delay_ostickspersec;  
	SysTick->CTRL|=SysTick_CTRL_TICKINT_Msk;
	SysTick->LOAD=reload;
	SysTick->CTRL|=SysTick_CTRL_ENABLE_Msk;
#else
#endif
}								    

#if SYSTEM_SUPPORT_OS    								   
void delay_us(u32 nus)
{		
	u32 ticks;
	u32 told,tnow,tcnt=0;
	u32 reload=SysTick->LOAD;
	ticks=nus*fac_us; 				
	delay_osschedlock();			
	told=SysTick->VAL;       
	while(1)
	{
		tnow=SysTick->VAL;	
		if(tnow!=told)
		{	    
			if(tnow<told)tcnt+=told-tnow;
			else tcnt+=reload-tnow+told;	
			told=tnow;
			if(tcnt>=ticks)break;
		}  
	};
	delay_osschedunlock();	
}  


void delay_ms(u16 nms)
{	
	if(delay_osrunning&&delay_osintnesting==0)   
	{		 
		if(nms>=fac_ms)
		{ 
   			delay_ostimedly(nms/fac_ms);
		}
		nms%=fac_ms;  
	}
	delay_us((u32)(nms*1000));
}
#else  

void delay_us(u32 nus)
{		
	u32 ticks;
	u32 told,tnow,tcnt=0;
	u32 reload=SysTick->LOAD;
	ticks=nus*fac_us; 			
	told=SysTick->VAL;       
	while(1)
	{
		tnow=SysTick->VAL;	
		if(tnow!=told)
		{	    
			if(tnow<told)tcnt+=told-tnow;
			else tcnt+=reload-tnow+told;	    
			told=tnow;
			if(tcnt>=ticks)break;
		}  
	};
}

void delay_ms(u16 nms)
{
	u32 i;
	for(i=0;i<nms;i++) delay_us(1000);
}
#endif








































