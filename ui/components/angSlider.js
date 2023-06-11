import { Slider } from '@mui/material';
import Box from '@mui/material/Box';
import React from 'react';


const AngSlider = ({ value, onChange }) => {

  function preventVerticalKeyboardNavigation(event) {
    if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
      event.preventDefault();
    }
  }

  const handleSliderChange = (event, newVal) => {
    onChange(newVal);
  };

  return (
    <>
      <h1>
        Angle
      </h1>
      <Box sx={{ width: 300, left: 50}}>
      <Slider
        sx={{
          '& input[type="range"]': {
            WebkitAppearance: 'slider-horizontal',
          },
        }}
        min={-15}
        max={15}
        step={0.01}
        orientation="horizontal"
        defaultValue={0}
        aria-label="Temperature"
        valueLabelDisplay="on"
        onKeyDown={preventVerticalKeyboardNavigation}
        onChange={handleSliderChange}
      />
      </Box>
    </>
    
  );
};

export default AngSlider;