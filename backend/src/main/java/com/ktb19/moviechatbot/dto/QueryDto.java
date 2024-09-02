package com.ktb19.moviechatbot.dto;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.ktb19.moviechatbot.constant.Constants;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.time.LocalDate;
import java.time.LocalTime;
import java.util.List;

import static com.ktb19.moviechatbot.constant.Constants.PATTERN_JSONFORMAT_DATE;
import static com.ktb19.moviechatbot.constant.Constants.PATTERN_JSONFORMAT_TIME;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class QueryDto {

    private String movieName;
    private List<String> region;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_DATE, timezone = "Asia/Seoul")
    private LocalDate date;

    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = PATTERN_JSONFORMAT_TIME, timezone = "Asia/Seoul")
    private LocalTime time;

    private String message;

    public static QueryDto of(AiInfosResponse aiInfosResponse) {

        String dateString = aiInfosResponse.getDate();
        LocalDate date = dateString == null ? null : LocalDate.parse(dateString);

        String timeString = aiInfosResponse.getTime();
        LocalTime time = timeString == null ? null : LocalTime.parse(timeString);

        return new QueryDto(
                aiInfosResponse.getMovieName(),
                aiInfosResponse.getRegion(),
                date,
                time,
                aiInfosResponse.getResponse()
        );
    }
}
