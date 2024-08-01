package com.ktb19.moviechatbot.dto;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.Setter;

import java.sql.Time;
import java.util.List;

@Getter
@Setter
@AllArgsConstructor
public class RunningTimesDto {

    private List<Time> times;
}
