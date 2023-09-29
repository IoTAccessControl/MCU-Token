
file(GLOB DevFiSrc  "../../../../MCUToken/iot_client/app/*.c"
	"../../../../MCUToken/iot_client/app/*.h"
	"../../../../MCUToken/iot_client/fp_gen/*.c"
	"../../../../MCUToken/iot_client/fp_gen/*.h"
)

set(DevFiInclude "../../../../MCUToken/iot_client/fp_gen/" "../../../../MCUToken/iot_client/app/")

idf_component_register(SRCS ${DevFiSrc}
	INCLUDE_DIRS ${DevFiInclude})

target_compile_options(${COMPONENT_TARGET} PUBLIC -DUSE_ESP32 -DDEV_ESP32_S2)