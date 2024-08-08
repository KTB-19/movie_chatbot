package com.ktb19.moviechatbot.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
public class MovieRunningTimesDto {

    private int count;
    private List<TheaterRunningTimesDto> theaterRunningTimes;

}
