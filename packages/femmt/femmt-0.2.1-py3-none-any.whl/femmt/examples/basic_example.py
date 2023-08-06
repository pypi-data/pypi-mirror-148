import femmt as fmt
import numpy as np

def example_thermal_simulation():
    # Thermal simulation:
    # The losses calculated by the magnetics simulation can be used to calculate the heat distribution of the given magnetic component
    # In order to use the thermal simulation, thermal conductivities for each material can be entered as well as a boundary temperature
    # which will be applied on the boundary of the simulation (dirichlet boundary condition).
    
    # The case parameter sets the thermal conductivity for a case which will be set around the core.
    # This could model some case in which the transformer is placed in together with a set potting material.
    thermal_conductivity_dict = {
            "air": 0.0263,
            "case": { # epoxy resign
                "top": 0.122,
                "top_right": 0.122,
                "right": 0.122,
                "bot_right": 0.122,
                "bot": 0.122
            },
            "core": 5, # ferrite
            "winding": 400, # copper
            "air_gaps": 180, # aluminiumnitride
            "isolation": 0.42 # polyethylen
    }

    # Here the case size can be determined
    case_gap_top = 0.002
    case_gap_right = 0.0025
    case_gap_bot = 0.002

    # Here the boundary temperatures can be set, currently it is set to 20°C (around 293°K).
    # This does not change the results of the simulation (at least when every boundary is set equally) but will set the temperature offset.
    boundary_temperatures = {
        "value_boundary_top": 20,
        "value_boundary_top_right": 20,
        "value_boundary_right_top": 20,
        "value_boundary_right": 20,
        "value_boundary_right_bottom": 20,
        "value_boundary_bottom_right": 20,
        "value_boundary_bottom": 20
    }
    
    # In order to compare the femmt thermal simulation with a femm heat flow simulation the same boundary temperature should be applied.
    # Currently only one temperature can be applied which will be set on every boundary site.
    femm_boundary_temperature = 20

    # Here the boundary sides can be turned on (1) or off (0)
    boundary_flags = {
        "flag_boundary_top": 1,
        "flag_boundary_top_right": 1,
        "flag_boundary_right_top": 1,
        "flag_boundary_right": 1,
        "flag_boundary_right_bottom": 1,
        "flag_boundary_bottom_right": 1,
        "flag_boundary_bottom": 1
    }

    # In order for the thermal simulation to work an electro_magnetic simulation has to run before.
    # The em-simulation will create a file containing the losses.
    # When the losses file is already created and contains the losses for the current model, it is enough to run geo.create_model in
    # order for the thermal simulation to work (geo.single_simulation is not needed).
    # Obviously when the model is modified and the losses can be out of date and therefore the geo.single_simulation needs to run again.
    geo.thermal_simulation(thermal_conductivity_dict, boundary_temperatures, boundary_flags, case_gap_top, case_gap_right, case_gap_bot, True)

    # Because the isolations inside of the winding window are not implemented in femm simulation.
    # The validation only works when the isolations for the FEMMT thermal simulation are turned off.
    # geo.femm_thermal_validation(thermal_conductivity_dict, femm_boundary_temperature, case_gap_top, case_gap_right, case_gap_bot)

component = "inductor"
# component = "transformer-interleaved"
# component = "integrated_transformer"
# component = "transformer"

# Create Object
if component == "inductor":
    # 1. chose simulation type
    geo = fmt.MagneticComponent(component_type="inductor")

    # 2. set core parameters
    core = fmt.core_database()["PQ 40/40"]
    #geo.core.update(window_h=0.04, window_w=0.00745,
    #                mu_rel=3100, phi_mu_deg=12,
    #                sigma=0.6)
    geo.core.update(core_w=core["core_w"], window_w=core["window_w"], window_h=core["window_h"],
                    mu_rel=3100, phi_mu_deg=12,
                    sigma=0.6)

    # 3. set air gap parameters
    geo.air_gaps.update(method="center", n_air_gaps=1, air_gap_h=[0.0005], position_tag=[0])

    geo.update_conductors(n_turns=[[8]], conductor_type=["solid"], conductor_radii=[0.0015],
                          winding=["primary"], scheme=["square"],
                          core_cond_isolation=[0.001, 0.001, 0.002, 0.001], cond_cond_isolation=[0.0001],
                          conductivity_sigma=["copper"])

    geo.create_model(freq=100000, visualize_before=True, do_meshing=True, save_png=False)

    geo.single_simulation(freq=100000, current=[3], show_results=True)

    # example_thermal_simulation()

    # Excitation Sweep Example
    # Perform a sweep using more than one frequency
    # fs = [0, 10000, 30000, 60000, 100000, 150000]
    # amplitude_list = [[10], [2], [1], [0.5], [0.2], [0.1]]
    # phase_list = [[0], [10], [20], [30], [40], [50]]
    # geo.excitation_sweep(frequency_list=fs, current_list_list=amplitude_list, phi_deg_list_list=phase_list)

    # Reference simulation using FEMM
    # geo.femm_reference(freq=100000, current=[1], sigma_cu=58, sign=[1], non_visualize=0)

if component == "transformer-interleaved":
    # 1. chose simulation type
    geo = fmt.MagneticComponent(component_type="transformer")

    # 2. set core parameters
    geo.core.update(window_h=0.0295, window_w=0.012, core_w=0.015,
                    non_linear=False, sigma=1, re_mu_rel=3200, phi_mu_deg=10)

    # 3. set air gap parameters
    geo.air_gaps.update(method="percent", n_air_gaps=1, air_gap_h=[0.0005],
                        air_gap_position=[50], position_tag=[0])

    # 4. set conductor parameters: use solid wires
    geo.update_conductors(n_turns=[[21], [7]], conductor_type=["solid", "solid"],
                        litz_para_type=['implicit_litz_radius', 'implicit_litz_radius'],
                        ff=[None, 0.6], strands_numbers=[None, 600], strand_radii=[70e-6, 35.5e-6],
                        conductor_radii=[0.0011, 0.0011],
                        winding=["interleaved"], scheme=["horizontal"],
                        core_cond_isolation=[0.001, 0.001, 0.002, 0.001], cond_cond_isolation=[0.0002, 0.0002, 0.0005],
                        conductivity_sigma=["copper", "copper"])

    # 4. set conductor parameters: use litz wires
    # geo.update_conductors(n_turns=[[21], [7]], conductor_type=["litz", "litz"],
    #                     litz_para_type=['implicit_litz_radius', 'implicit_litz_radius'],
    #                     ff=[0.6, 0.6], strands_numbers=[600, 600], strand_radii=[35.5e-6, 35.5e-6],
    #                     conductor_radii=[0.0011, 0.0011],
    #                     winding=["interleaved"], scheme=["horizontal"],
    #                     core_cond_isolation=[0.001, 0.001, 0.002, 0.001], cond_cond_isolation=[0.0002, 0.0002, 0.0005],
    #                     conductivity_sigma=["copper", "copper"])

    # 5. start simulation with given frequency, currents and phases
    geo.create_model(freq=250000, visualize_before=True)
    geo.single_simulation(freq=250000, current=[4, 12], phi_deg=[0, 180], show_results=True)


    # other simulation options:
    # ------------------------
    # read inductances
    # geo.get_inductances(I0=8, op_frequency=250000, skin_mesh_factor=0.5)

    # perform a reference simulation using FEMM
    # geo.femm_reference(freq=250000, current=[4, 12], sign=[1, -1], non_visualize=0)

    example_thermal_simulation()
    

if component == "transformer":
    # Example for a transformer with multiple virtual winding windows.

    # 1. chose simulation type
    geo = fmt.MagneticComponent(component_type="transformer")

    # 2. set core parameters
    geo.core.update(window_h=0.0295, window_w=0.012, core_w=0.015,
                    mu_rel=3100, phi_mu_deg=12,
                    sigma=0.6)

    # 3. set air gap parameters
    geo.air_gaps.update(method="percent", n_air_gaps=1, air_gap_h=[0.0005],
                        air_gap_position=[50], position_tag=[0])

    # 4. set conductor parameters
    geo.update_conductors(n_turns=[[10, 0], [0, 10]], conductor_type=["solid", "litz"],
                        litz_para_type=['implicit_litz_radius', 'implicit_litz_radius'],
                        ff=[None, 0.6], strands_numbers=[None, 600], strand_radii=[70e-6, 35.5e-6],
                        conductor_radii=[0.0011, None],
                        winding=["primary", "secondary"], scheme=["square", "square"],
                        core_cond_isolation=[0.001, 0.001, 0.002, 0.001], cond_cond_isolation=[0.0002, 0.0002, 0.0005],
                        conductivity_sigma=["copper", "copper"])

    # 5. start simulation with given frequency, currents and phases
    geo.create_model(freq=250000, visualize_before=True)
    geo.single_simulation(freq=250000, current=[4.14723021, 14.58960019], phi_deg=[- 1.66257715/np.pi*180, 170])

if component == "integrated_transformer":
    # 1. chose simulation type
    geo = fmt.MagneticComponent(component_type="integrated_transformer")

    # 2. set core parameters
    geo.core.update(window_h=0.03, window_w=0.011,
                    mu_rel=3100, phi_mu_deg=12,
                    sigma=0.6)

    # 2.1 set stray path parameters
    geo.stray_path.update(start_index=0,
                          radius=geo.core.core_w / 2 + geo.core.window_w - 0.001)

    # 3. set air gap parameters
    geo.air_gaps.update(method="percent",
                        n_air_gaps=2,
                        position_tag=[0, 0],
                        air_gap_h=[0.001, 0.001],
                        air_gap_position=[30, 40])

    # 4. set conductor parameters
    geo.update_conductors(n_turns=[[1, 3], [2, 6]], conductor_type=["litz", "litz"],
                          litz_para_type=['implicit_litz_radius', 'implicit_litz_radius'],
                          ff=[0.5, 0.5], strands_numbers=[100, 100], strand_radii=[70e-6, 70e-6],
                          winding=["interleaved", "interleaved"], scheme=["horizontal", "horizontal"],
                          core_cond_isolation=[0.001, 0.001, 0.002, 0.001], cond_cond_isolation=[0.0002, 0.0002, 0.0005],
                          conductivity_sigma=["copper", "copper"])

    # 5. start simulation with given frequency, currents and phases
    geo.create_model(freq=250000, visualize_before=True)
    geo.single_simulation(freq=250000, current=[8.0, 4.0], phi_deg=[0, 180])

    # other simulation options:
    # -------------------------
    # geo.get_inductances(I0=10, op_frequency=100000, skin_mesh_factor=0.5)
