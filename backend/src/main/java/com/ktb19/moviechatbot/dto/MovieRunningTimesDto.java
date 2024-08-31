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

    @Schema(description = "상영 정보 메세지",
            example = """
                    현재 위치에서 가장 가까운 영화관들 중에서 추천드릴 수 있는 영화관은 다음과 같습니다:
                    1. CGV 성남모란
                       - 영화: 에이리언: 로물루스
                       - 상영 시간: 12:45, 17:15, 19:30
                       - 총 3회 상영
                       - 위치: 모란역 1번 출구에서 도보로 3분 거리

                    2. CGV 서현
                       - 영화: 에이리언: 로물루스
                       - 상영 시간: 17:00, 20:00
                       - 총 2회 상영
                       - 위치: 서현역 2번 출구에서 도보로 5분 거리

                    3. CGV 야탑
                       - 영화: 에이리언: 로물루스
                       - 상영 시간: 17:00
                       - 총 1회 상영
                       - 위치: 야탑역 3번 출구에서 도보로 2분 거리

                    각 영화관 위치에 대한 설명과 대중교통을 이용한 접근법을 참고해주세요. 좋은 영화 감상하시길 바랍니다!
            """)
    private String message;

}
