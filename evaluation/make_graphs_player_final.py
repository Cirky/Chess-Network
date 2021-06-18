import matplotlib.pyplot as plt

X = [0.001, 0.05, 0.1, 0.2, 0.3]
player_net_Y = [0.8227157016736175, 0.7499886859413877, 0.7292082189449077, 0.6881715795277087, 0.6658006072998148]
player_net_E = [0.011659211408624052, 0.010697731837625587, 0.006865301227898141, 0.004297532253996203, 0.007849651395912116]
player_shannon_Y = [0.8828098639721886, 0.8051269971581302, 0.7811394654696818, 0.7463071278596323, 0.7194186236360733]
player_shannon_E = [0.009620173186722767, 0.010654712889755254, 0.012755927752956022, 0.01681578836401625, 0.018357294341697798]

computer_net_Y = [0.8926000000000001, 0.8822055924905463, 0.8718899990437741, 0.8364792763275883, 0.7996420728649299]
computer_net_E = [0.013951344021276242, 0.011206552316426565, 0.010201134689325767, 0.009489075334949923, 0.008330386356456915]
computer_shannon_Y = [0.892, 0.8473192367558428, 0.8047090925284259, 0.7637999228076783, 0.7454881594830385]
computer_shannon_E = [0.00827042925125414, 0.01741161759447908, 0.0293570430645685, 0.025474219077528875, 0.02901108745310524]

xlabels = ["last move", 0.05, 0.10, 0.20, 0.30]

plt.figure(figsize=(8, 5))
plt.rcParams.update({'font.size': 11})
plt.xlabel("Moves from end")
plt.ylabel("Accuracy ($\mu \pm \sigma$)")
plt.errorbar(X, player_net_Y, player_net_E, linestyle="--", marker='^', markersize="6", label="Human games - Advanced color-separated network",
             linewidth=0.8)
plt.errorbar(X, player_shannon_Y, player_shannon_E, linestyle="--", marker='v', markersize="6", label="Human games - "
                                                                                                      "Shannon function",
             linewidth=0.8)
plt.errorbar(X, computer_net_Y, computer_net_E, linestyle="--", marker='o', markersize="6", label="AI games - "
                                                                                                  "Advanced color-separated network", linewidth=0.8)
plt.errorbar(X, computer_shannon_Y, computer_shannon_E, linestyle="--", marker='D', markersize="6", label="AI games - Shannon function",
             linewidth=0.8)
plt.xticks(X, labels=xlabels)
plt.ylim([0.6, 0.92])
plt.legend()
plt.savefig("../output/graphs/final.png")
plt.show()