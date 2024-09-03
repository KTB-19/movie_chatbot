package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import io.swagger.v3.oas.annotations.media.Schema;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

import static com.ktb19.moviechatbot.constant.Constants.PATTERN_JSONFORMAT_DATE;
import static com.ktb19.moviechatbot.constant.Constants.PATTERN_JSONFORMAT_TIME;

@Schema(description = "메시지 파싱 응답")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class ParsedQueryResponse {

    @Schema(description = "영화 이름", example = "에이리언 : 로물루스")
    private String movieName;

    @Schema(description = "지역", example = "null")
    private List<String> region;

    @Schema(description = "상영 날짜", example = "2024-08-14")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_DATE, timezone = "Asia/Seoul")
    private LocalDate date;

    @Schema(description = "상영 시간", example = "17:00", type = "string")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_TIME, timezone = "Asia/Seoul")
    private LocalTime time;

    @Schema(description = "서비스 답변", example = "어느 지역에서 영화를 보고 싶으신가요?")
    private String message;

    public static ParsedQueryResponse of(QueryDto dto) {
        return new ParsedQueryResponse(
                dto.getMovieName(),
                dto.getRegion(),
                dto.getDate(),
                dto.getTime(),
                dto.getMessage()
        );
    }

}
