import {useEffect, useState} from "react";

const areas = [
    {
        wideArea: "서울시",
        basicArea: [
            "강남구",
            "강동구",
            "강북구",
            "강서구",
            "관악구",
            "광진구",
            "구로구",
            "금천구",
            "노원구",
            "도봉구",
            "동대문구",
            "동작구",
            "마포구",
            "서대문구",
            "서초구",
            "성동구",
            "성북구",
            "송파구",
            "양천구",
            "영등포구",
            "용산구",
            "은평구",
            "종로구",
            "중구",
            "중랑구",
        ]
    },
    {
        wideArea: "경기도",
        basicArea: [
            "광주시",
            "구리시",
            "군포시",
            "김포시",
            "남양주시",
            "동두천시",
            "부천시",
            "성남시",
            "수원시",
            "시흥시",
            "안산시",
            "안성시",
            "안양시",
            "오산시",
            "용인시",
            "의왕시",
            "의정부시",
            "이천시",
            "파주시",
            "평택시",
            "하남시",
            "화성시",
            "가평군",
            "양주시",
            "양평군",
            "여주군",
            "연천군",
            "포천시",
            "고양시",
            "과천시",
            "광명시",
        ]
    },
    {
        wideArea: "강원도",
        basicArea: [
            "양양군",
            "영월군",
            "인제군",
            "정선군",
            "철원군",
            "평창군",
            "홍천군",
            "화천군",
            "횡성군",
            "강릉시",
            "동해시",
            "삼척시",
            "속초시",
            "원주시",
            "춘천시",
            "태백시",
            "고성군",
            "양구군",
        ]
    },
    {
        wideArea: "충청북도",
        basicArea: [
            "제천시",
            "청주시",
            "충주시",
            "괴산군",
            "단양군",
            "보은군",
            "영동군",
            "옥천군",
            "음성군",
            "진천군",
            "청원군",
            "증평군",
        ]
    },
    {
        wideArea: "충청남도",
        basicArea: [
            "공주시",
            "논산시",
            "보령시",
            "서산시",
            "아산시",
            "천안시",
            "금산군",
            "당진군",
            "부여군",
            "서천군",
            "예산군",
            "청양군",
            "태안군",
            "홍성군",
            "계룡시",
        ]
    },
    {
        wideArea: "경상북도",
        basicArea: [
            "경산시",
            "경주시",
            "구미시",
            "김천시",
            "문경시",
            "상주시",
            "안동시",
            "영주시",
            "영천시",
            "포항시",
            "고령군",
            "군위군",
            "봉화군",
            "성주군",
            "영덕군",
            "영양군",
            "예천군",
            "울릉군",
            "울진군",
            "의성군",
            "청도군",
            "청송군",
            "칠곡군",
        ]
    },
    {
        wideArea: "경상남도",
        basicArea: [
            "합천군",
            "창원시 마산합포구",
            "창원시 마산회원구",
            "창원시 성산구",
            "창원시 의창구",
            "창원시 진해구",
            "거제시",
            "김해시",
            "밀양시",
            "사천시",
            "양산시",
            "진주시",
            "창원시",
            "통영시",
            "거창군",
            "고성군",
            "남해군",
            "산청군",
            "의령군",
            "창녕군",
            "하동군",
            "함안군",
            "함양군",
        ]
    },
    {
        wideArea: "전라북도",
        basicArea: [
            "진안군",
            "군산시",
            "김제시",
            "남원시",
            "익산시",
            "전주시",
            "정읍시",
            "고창군",
            "무주군",
            "부안군",
            "순창군",
            "완주군",
            "임실군",
            "장수군",
        ]
    },
    {
        wideArea: "전라남도",
        basicArea: [
            "광양시",
            "나주시",
            "목포시",
            "순천시",
            "여수시",
            "강진군",
            "고흥군",
            "곡성군",
            "구례군",
            "담양군",
            "무안군",
            "보성군",
            "신안군",
            "영광군",
            "영암군",
            "완도군",
            "장성군",
            "장흥군",
            "진도군",
            "함평군",
            "해남군",
            "화순군",
        ]
    },
    {
        wideArea: "제주도",
        basicArea: [
            "서귀포시",
            "제주시",
            "남제주군",
            "북제주군",
        ]
    },
    {
        wideArea: "부산시",
        basicArea: [
            "강서구",
            "금정구",
            "남구",
            "동구",
            "동래구",
            "부산진구",
            "북구",
            "사상구",
            "사하구",
            "서구",
            "수영구",
            "연제구",
            "영도구",
            "중구",
            "해운대구",
            "기장군",
        ]
    },
    {
        wideArea: "대구시",
        basicArea: [
            "남구",
            "달서구",
            "동구",
            "북구",
            "서구",
            "수성구",
            "중구",
            "달성군",
        ]
    },
    {
        wideArea: "대전시",
        basicArea: [
            "대덕구",
            "동구",
            "서구",
            "유성구",
            "중구",
        ]
    },
    {
        wideArea: "울산시",
        basicArea: [
            "남구",
            "동구",
            "북구",
            "중구",
            "울주군",
        ]
    },
    {
        wideArea: "인천시",
        basicArea: [
            "계양구",
            "남구",
            "남동구",
            "동구",
            "부평구",
            "서구",
            "연수구",
            "중구",
            "강화군",
            "웅진군",
        ]
    },
    {
        wideArea: "광주시",
        basicArea: [
            "광산구",
            "남구",
            "동구",
            "북구",
            "서구"
        ]
    },
    {
        wideArea: "세종시",
        basicArea: [
            "연기군",
        ]
    },
]

const RegionSelector = () => {

    const [wideArea, setWideArea] = useState("");
    const [basicArea, setBasicArea] = useState("");
    const [basicAreas, setBasicAreas] = useState([]);

    const handleWideAreaChange = (e) => {
        setWideArea(e.target.value);
    };

    useEffect(() => {
        setBasicAreas(areas.find((area) => area.wideArea === wideArea)?.basicArea || []);
    }, [wideArea]);

    const handleBasicAreaChange = (e) => {
        setBasicArea(e.target.value);
    };

    return (
        <div className="regionSelector">
            <select value={wideArea} onChange={handleWideAreaChange}>
                <option value="">지역을 선택해주세요</option>
                {areas.map((area) => (
                    <option key={area.wideArea} value={area.wideArea}>
                        {area.wideArea}
                    </option>
                ))}
            </select>
            <select value={basicArea} onChange={handleBasicAreaChange}>
                <option value="">시,군,구를 선택해주세요</option>
                {basicAreas.map((area) => (
                    <option key={area} value={area}>
                        {area}
                    </option>
                ))}
            </select>
        </div>
    );
};
export default RegionSelector;