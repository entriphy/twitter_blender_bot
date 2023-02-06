import json
import os
import UnityPy
from UnityPy.classes import MonoBehaviour, MonoScript

if __name__ == "__main__":
    infos = {}

    # Load config from json file
    with open("config.json", "r") as f:
        config = json.load(f)
    
    # Read every specified chr file
    for id in config["kprs_chrs"]:
        env = UnityPy.load(os.path.join(config["kprs_path"], "Klonoa_Data", "StreamingAssets", "Klonoa2", "StandaloneWindows64", "chr_infos", "remake", "chr_" + id))

        # Find ActStateInfos behaviour
        for obj in env.objects:
            if obj.type.name == "MonoBehaviour":
                behaviour: MonoBehaviour = obj.read()
                script: MonoScript = behaviour.m_Script.read()
                if script.name == "ActStateInfos":
                    # Write every animation description to infos dict
                    tree = behaviour.read_typetree()
                    for anim in tree["infos"]:
                        infos[anim["name"]] = anim["remarks"]

    # Write dict to json file
    with open("infos.json", "w", encoding="utf-8") as f:
        json.dump(infos, f, indent=4, ensure_ascii=False)
