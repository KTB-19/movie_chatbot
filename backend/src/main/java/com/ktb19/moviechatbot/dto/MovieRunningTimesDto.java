package com.ktb19.moviechatbot.dto;

import io.swagger.v3.oas.annotations.media.ArraySchema;
import io.swagger.v3.oas.annotations.media.ExampleObject;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Schema(description = "상영 정보 응답")
@Getter
@Setter
@AllArgsConstructor
public class MovieRunningTimesDto {

    @Schema(description = "영화관 개수", example = "2")
    private int count;

    @Schema(description = "영화관", type = "array",
            example = "[{ \"theaterName\": \"CGV 동성로\", \"count\": 3, \"times\": [\"17:00\", \"18:30\", \"19:00\"]}," +
                    "{ \"theaterName\": \"롯데시네마 대구\", \"count\": 2, \"times\": [\"18:00\", \"20:00\"] }]")
    private List<TheaterRunningTimesDto> theaterRunningTimes;

}
