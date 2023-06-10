import { Slider } from '@mui/material';
import Box from '@mui/material/Box';
import React from 'react';



const ThrustSlider = ({ value, onChange }) => {
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
        Thrust
      </h1>
      <Box sx={{ width: 300}}>
      <Slider
        sx={{
          '& input[type="range"]': {
            WebkitAppearance: 'slider-horizontal',
          },
        }}
        min={0}
        max={1}
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

export default ThrustSlider;