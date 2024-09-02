package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.ktb19.moviechatbot.constant.Constants;
import io.swagger.v3.oas.annotations.media.Schema;
import jakarta.validation.constraints.Pattern;
import jakarta.validation.constraints.Size;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalTime;

import static com.ktb19.moviechatbot.constant.Constants.*;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ParsedQueryRequest {

    @Schema(description = "영화 이름", example = "에이리언 : 로물루스")
    @Pattern(regexp = PATTERN_REGEXP_ALL, message = PATTERN_REGEXP_ALL_MESSAGE)
    @Size(max = 100)
    private String movieName;

    @Schema(description = "지역", example = "null")
    @Pattern(regexp = PATTERN_REGEXP_KOREAN, message = PATTERN_REGEXP_KOREAN_MESSAGE)
    @Size(max = 30)
    private String region;

    @Schema(description = "상영 날짜", example = "2024-08-14")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_DATE, timezone = "Asia/Seoul")
    private LocalDate date;

    @Schema(description = "상영 시간", example = "17:00", type = "string")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_TIME, timezone = "Asia/Seoul")
    private LocalTime time;

}
